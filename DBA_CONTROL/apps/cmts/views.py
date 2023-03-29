from django.db import connection, transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from cmts.models import College, Teacher, Major, Student
from cmts.serializers import CollegeSerializer, MajorSerializer, TeacherSerializer, StudentSerializer


class CollegeViewSet(DestroyModelMixin, GenericViewSet):
    """学院信息增删改查 模糊查"""
    # 只有删不涉及其他表，只用获取ID删除COLLEGE
    # list需要查询Teacher表，update修改院长需查询Teacher表，create需查院长存不存在和pop院长，search涉及院长姓名查询
    permission_classes = [IsAuthenticated]
    serializer_class = CollegeSerializer

    def get_queryset(self):  # 没有query自己制造query
        # select * from college
        return College.objects.all()

    # GET /college/
    def list(self, request, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute("select c.id, c.name, t.name, c.content from gdut_college c, gdut_teacher t where c.dean_id = t.id")
        tuples = cursor.fetchall()
        data = []
        for tup in tuples:
            data.append({"id": tup[0], "ip": tup[1], "source": tup[2], "content": tup[3]})

        return Response({'college': data})

    # DELETE /college/<pk>/
    # destroy交给DestroyModelMixin了，但注意前端传入必须为ID（pk字段才匹配得上）

    # PUT /college/<pk>/JSON内容
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()  # 这里通过pk获取到数据库对应的实例，但这里拿进来的dean_name是匹配不上的
        # 需先判断一下 dean_id和dean_name存不存在或匹不匹配得上
        # select count(*) from teacher where id = dean_id and name = dean_name;
        if Teacher.objects.filter(id=request.data["dean_id"], name=request.data["dean_name"]).count() == 0:
            return Response({"message": "院长ID与姓名或有误"}, status=status.HTTP_400_BAD_REQUEST)
        request.data.pop("dean_name")

        # request.data能恰好取出前端的json格式
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # update college set dean_id = dean_id, content = content where id = id
        serializer.save()  # self.perform_update(serializer) 源码里面的
        return Response(serializer.data)

    # POST /college/
    # POST请求方式，数据为全新新增的，故不需要带*args, **kwargs
    def create(self, request):
        # select count(*) from teacher where id = dean_id and name = dean_name;
        if Teacher.objects.filter(id=request.data["dean_id"], name=request.data["dean_name"]).count() == 0:
            return Response({"message": "院长ID与姓名或有误"}, status=status.HTTP_400_BAD_REQUEST)
        request.data.pop("dean_name")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # GET /college/search/?xxx 模糊查询
    @action(methods=['get'], detail=False)
    def search(self, request):
        data = []
        cursor = connection.cursor()
        sql = ''
        if 'college_name' in request.GET:
            college_name = '%' + request.GET.get('college_name') + '%'  # 需要%s为'%s'，否则识别不出来
            sql = "select c.id, c.name, t.name, c.content from gdut_college c, gdut_teacher t where c.dean_id = t.id and c.name like '%s'" % college_name
        elif 'dean_name' in request.GET:
            dean_name = '%' + request.GET.get('dean_name') + '%'
            sql = "select c.id, c.name, t.name, c.content from gdut_college c, gdut_teacher t where c.dean_id = t.id and t.name like '%s'" % dean_name
        elif 'content' in request.GET:
            content = '%' + request.GET.get('content') + '%'
            sql = "select c.id, c.name, t.name, c.content from gdut_college c, gdut_teacher t where c.dean_id = t.id and c.content like '%s'" % content
        else:
            return Response({"message": "搜索信息有误"}, status=status.HTTP_400_BAD_REQUEST)  # 搜索信息为空的情况在前端已被拦
        cursor.execute(sql)
        for tup in cursor.fetchall():
            data.append({"id": tup[0], "ip": tup[1], "source": tup[2], "content": tup[3]})
        return Response({'college': data})


class MajorViewSet(DestroyModelMixin, GenericViewSet):
    """专业信息增删改查 模糊查"""
    # 只有删和改不涉及其他表，只用获取ID删除Major（改的时候是改不了院长名和专业名和专业人数的，只能改简介，只涉及major表）
    # 但UpdateModelMixin对于只改变某些字段的情况不合适，因为另外不修改的字段可能不能直接从前端传入，还需要查库，但这个mixin需要
    # list需要查询college表与grade表（专业人数），create需查学院存不存在和pop学院和获取学院ID入库 与 专业人数对不对得上（查grade表）与 专业与学院对不对得上，search涉及学院名称查询
    permission_classes = [IsAuthenticated]
    serializer_class = MajorSerializer

    def get_queryset(self):
        # select * from major
        return Major.objects.all()

    # GET /major/
    def list(self, request, *args, **kwargs):
        cursor = connection.cursor()
        # select m.id, m.name, c.name, m.content from gdut_major m, gdut_college c where m.college_id = c.id
        cursor.execute("select m.id, m.name, c.name, m.content from gdut_major m, gdut_college c where m.college_id = c.id")
        tuples = cursor.fetchall()
        data = []
        for tup in tuples:
            cursor.execute("select sum(count) from gdut_grade where major_id = '%s'", tup[0])
            count = cursor.fetchone()[0]
            if count is None:
                count = 0
            data.append({"id": tup[0], "ip": tup[1], "source": tup[2], "content": tup[3], "count": count})

        return Response({'major': data})

    # POST /major/
    # POST请求方式，数据为全新新增的，故不需要带*args, **kwargs
    # 查看专业名称是否存在，学院名称是否存在，专业人数是否正确
    def create(self, request):
        # select count(*) from gdut_major where name = name;  -- 传入的name就是major name
        if Major.objects.filter(name=request.data["name"]).count() > 0:
            return Response({"message": "专业已存在"}, status=status.HTTP_400_BAD_REQUEST)

        cursor = connection.cursor()
        cursor.execute("select id from gdut_college where name = '%s'" % request.data["college_name"])
        tuple_info = cursor.fetchone()
        # select count(*) from gdut_college where name = college_name;
        if tuple_info is None:
            return Response({"message": "学院不存在"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data["count"] == 0:
            return Response({"message": "专业初始化人数必须为0"}, status=status.HTTP_400_BAD_REQUEST)

        request.data['college_id'] = tuple_info[0]
        request.data.pop("college_name")
        request.data.pop("count")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # PUT /major/<pk>/JSON内容  只需改变content内容即可，所以不需使用序列化器（因为不改动的字段college_id需要多查库college）
    def update(self, request, *args, **kwargs):
        # instance = self.get_object()  # 这里通过pk获取到数据库对应的实例，但并不需要
        # update gdut_major set content=content where name = name
        cursor = connection.cursor()
        cursor.execute("update gdut_major set content='%s' where name = '%s'" %
                       (request.data["content"], request.data["name"]))
        return Response(status=status.HTTP_200_OK)

    # GET /major/search/?xxx 模糊查询
    @action(methods=['get'], detail=False)
    def search(self, request):
        data = []
        cursor = connection.cursor()
        if 'college_name' in request.GET:
            college_name = '%' + request.GET.get('college_name') + '%'  # 需要%s为'%s'，否则识别不出来
            cursor.execute(
                "select m.id, m.name, c.name, m.content from gdut_major m, gdut_college c where m.college_id = c.id and c.name like '%s'" % college_name)
        elif 'name' in request.GET:
            name = '%' + request.GET.get('name') + '%'
            cursor.execute(
                "select m.id, m.name, c.name, m.content from gdut_major m, gdut_college c where m.college_id = c.id and m.name like '%s'" % name)
        elif 'content' in request.GET:
            content = '%' + request.GET.get('content') + '%'
            cursor.execute(
                "select m.id, m.name, c.name, m.content from gdut_major m, gdut_college c where m.college_id = c.id and m.content like '%s'" % content)
        else:
            return Response({"message": "搜索信息有误"}, status=status.HTTP_400_BAD_REQUEST)  # 搜索信息为空的情况在前端已被拦

        for tup in cursor.fetchall():
            cursor.execute("select count(*) from gdut_grade where gdut_grade.major_id = '%s'", tup[0])
            count = cursor.fetchone()[0]
            data.append({"id": tup[0], "ip": tup[1], "source": tup[2], "content": tup[3], "count": count})
        return Response({'major': data})


class TeacherViewSet(DestroyModelMixin, GenericViewSet):
    """教师信息增删改查 模糊查"""
    # destroy只需教师ID
    # update涉及更改学院，create也涉及学院，list同理，模糊查√
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer

    def get_queryset(self):
        # select * from major
        return Teacher.objects.all()

    # GET /teacher/
    def list(self, request, *args, **kwargs):
        cursor = connection.cursor()
        sql = "select t.id, t.name, c.name, t.content from gdut_teacher t, gdut_college c where t.college_id = c.id"
        cursor.execute(sql)
        data = []
        for tup in cursor.fetchall():
            data.append({"id": tup[0], "ip": tup[1], "source": tup[2], "content": tup[3]})
        return Response({'teacher': data})

    # POST /teacher/
    # POST请求方式，数据为全新新增的，故不需要带*args, **kwargs
    # 学院名称是否存在，教师ID是否存在过（存在再添加就矛盾了）
    def create(self, request):
        # select count(*) from gdut_teacher where name = name;  -- 传入的name就是major name
        if Teacher.objects.filter(name=request.data["id"]).count() > 0:
            return Response({"message": "教师号已存在，请勿重复添加"}, status=status.HTTP_400_BAD_REQUEST)
        if len(request.data['id']) != 10:
            return Response({"message": "教师工号必须为10位"}, status=status.HTTP_400_BAD_REQUEST)

        cursor = connection.cursor()
        cursor.execute("select id from gdut_college where name = '%s'" % request.data["college_name"])
        tuple_info = cursor.fetchone()
        if tuple_info is None:
            return Response({"message": "学院不存在"}, status=status.HTTP_400_BAD_REQUEST)

        request.data['college_id'] = tuple_info[0]
        request.data.pop("college_name")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # PUT /teacher/<pk>/JSON内容
    # 只可改变所属学院和content
    def update(self, request, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute("select id from gdut_college where name = '%s'" % request.data["college_name"])
        tuple_info = cursor.fetchone()
        if tuple_info is None:
            return Response({"message": "学院不存在"}, status=status.HTTP_400_BAD_REQUEST)

        college_id = tuple_info[0]

        cursor.execute("update gdut_teacher set college_id = %s, content='%s' where id = '%s'" %
                       (college_id, request.data["content"], request.data["id"]))
        return Response(status=status.HTTP_200_OK)

    # GET /teacher/search/?xxx 模糊查询
    @action(methods=['get'], detail=False)
    def search(self, request):
        data = []
        cursor = connection.cursor()
        if 'college_name' in request.GET:
            college_name = '%' + request.GET.get('college_name') + '%'
            sql = "select t.id, t.name, c.name, t.content from gdut_teacher t, gdut_college c where t.college_id = c.id and c.name like '%s'" % college_name
        elif 'name' in request.GET:
            name = '%' + request.GET.get('name') + '%'
            sql = "select t.id, t.name, c.name, t.content from gdut_teacher t, gdut_college c where t.college_id = c.id and t.name like '%s'" % name
        elif 'id' in request.GET:
            id = '%' + request.GET.get('id') + '%'
            sql = "select t.id, t.name, c.name, t.content from gdut_teacher t, gdut_college c where t.college_id = c.id and t.id like '%s'" % id
        elif 'content' in request.GET:
            content = '%' + request.GET.get('content') + '%'
            sql = "select t.id, t.name, c.name, t.content from gdut_teacher t, gdut_college c where t.college_id = c.id and t.content like '%s'" % content
        else:
            return Response({"message": "搜索信息有误"}, status=status.HTTP_400_BAD_REQUEST)  # 搜索信息为空的情况在前端已被拦
        cursor.execute(sql)
        for tup in cursor.fetchall():
            data.append({"id": tup[0], "ip": tup[1], "source": tup[2], "content": tup[3]})
        return Response({'teacher': data})


def check_grade_id(cursor, grade_id):
    """判断班级ID是否存在"""
    cursor.execute("select id from gdut_grade where id = '%s'" % grade_id)
    if cursor.fetchone() is None:
        return Response({"message": "班级ID不存在"}, status=status.HTTP_400_BAD_REQUEST)


def check_exist_student_id(cursor, id):
    """判断学号是否存在"""
    if len(id) != 10:
        return Response({"message": "学号应为十位数"}, status=status.HTTP_400_BAD_REQUEST)
    cursor.execute("select name from gdut_student where id = '%s'" % id)
    if cursor.fetchone() is None:
        return Response({"message": "学号已存在"}, status=status.HTTP_400_BAD_REQUEST)


def student_count_control(cursor, id, control):
    """学生人数存在 destroy-1 create+1"""
    cursor.execute("select grade_id, id from gdut_student where id = '%s'" % id)
    grade_id = cursor.fetchone()[0]
    if control == 'destroy':
        cursor.execute("update gdut_grade set count = count - 1 where id = '%s'" % grade_id)
    elif control == 'create':
        cursor.execute("update gdut_grade set count = count + 1 where id = '%s'" % grade_id)


class StudentViewSet(DestroyModelMixin, GenericViewSet):
    """
    学生信息增删改查 模糊查
    list: 展示 学号（id） 姓名（name） 简介（content） 届号（year） 学院（college_name） 专业（major_name）
            班级号（grade_number） 班级ID（grade_id）
    destroy: 删除，对应的班级人数减1
    update：改，学号（id）不能改，姓名、班级ID、简介可改，需判断班级ID存不存在，学号存在过
    create: id name grade_id content，需判断班级ID存不存在，学号存在过
    search:
    """
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer

    def get_queryset(self):
        # select * from gdut_student
        return Student.objects.all()

    # GET /student/
    def list(self, request, *args, **kwargs):
        cursor = connection.cursor()
        sql = "select s.id, s.name, s.content, g.year, c.name, m.name, g.grade_number, g.id from " \
              "gdut_student s, gdut_grade g, gdut_college c, gdut_major m where g.college_id = c.id and " \
              "g.major_id = m.id and s.grade_id = g.id"
        cursor.execute(sql)
        tuples = cursor.fetchall()
        data = []
        for tup in tuples:
            data.append({"id": tup[0], "name": tup[1], "content": tup[2], "year": tup[3], "college_name": tup[4],
                         "major_name": tup[5], "grade_number": tup[6], "grade_id": tup[7]})
        return Response({'student': data})

    # DELETE /student/<pk>/
    def destroy(self, request, *args, **kwargs):
        student_count_control(connection.cursor(), kwargs['pk'], "destroy")
        super().destroy(self, request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)  # 即使父类方法有但仍需补充Response，否则报错

    # PUT /student/<pk>/JSON内容
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        cursor = connection.cursor()
        check_grade_id(cursor, request.data["grade_id"])

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # update gdut_student set name=name, grade_id=grade_id, content=content where id = id
        serializer.save()
        data = dict(serializer.data)

        if request.data['change_grade_id'] == '2':  # 说明grade_id被改过
            cursor.execute(
                "select g.year, c.name, m.name, c.grade_number from gdut_grade g, gdut_college c, gdut_major m "
                "where g.college_id = c.id and g.major_id = m.id and g.id = '%s'" % request.data["grade_id"])
            tup = cursor.fetchone()
            data["year"] = tup[0]
            data["college_name"] = tup[1]
            data["major_name"] = tup[2]
            data["grade_number"] = tup[3]

        return Response(data)

    # POST /student/
    # 传入 id name grade_id content，但传出时需带上届号（year） 学院（college_name） 专业（major_name）班级号（grade_number）
    @transaction.atomic
    def create(self, request):
        cursor = connection.cursor()
        check_grade_id(cursor, request.data["grade_id"])
        check_exist_student_id(cursor, request.data["id"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        student_count_control(cursor, request.data["id"], "create")

        cursor.execute("select g.year, c.name, m.name, g.grade_number from gdut_grade g, gdut_college c, gdut_major m "
                       "where g.college_id = c.id and g.major_id = m.id and g.id = '%s'" % request.data["grade_id"])
        tup = cursor.fetchone()
        data = dict(serializer.data)  # 因为serializer.data为ReturnDict不能被像dict直接修改
        data["year"] = tup[0]
        data["college_name"] = tup[1]
        data["major_name"] = tup[2]
        data["grade_number"] = tup[3]
        return Response(data, status=status.HTTP_201_CREATED)

    # GET /student/search/?xxx 模糊查询
    @action(methods=['get'], detail=False)
    def search(self, request):
        data = []
        cursor = connection.cursor()
        sql = "select s.id, s.name, s.content, g.year, c.name, m.name, g    .grade_number, g.id from " \
              "gdut_student s, gdut_grade g, gdut_college c, gdut_major m where g.college_id = c.id and " \
              "g.major_id = m.id and s.grade_id = g.id"
        if 'id' in request.GET:
            sql = sql + " and s.id like '%s'" % ('%' + request.GET.get('id') + '%')
        elif 'name' in request.GET:
            sql = sql + " and s.name like '%s'" % ('%' + request.GET.get('name') + '%')
        elif 'content' in request.GET:
            sql = sql + " and s.content like '%s'" % ('%' + request.GET.get('content') + '%')
        elif 'year' in request.GET:
            sql = sql + " and g.year like %s" % ('%' + request.GET.get('year') + '%')
        elif 'college_name' in request.GET:
            sql = sql + " and c.name like '%s'" % ('%' + request.GET.get('college_name') + '%')
        elif 'major_name' in request.GET:
            sql = sql + " and m.name like '%s'" % ('%' + request.GET.get('major_name') + '%')
        elif 'grade_number' in request.GET:
            sql = sql + " and c.grade_number = %s" % str(int(request.GET.get('grade_number')))
        elif 'grade_id' in request.GET:
            sql = sql + " and g.id = %s" % str(int(request.GET.get('grade_id')))
        else:
            return Response({"message": "搜索信息有误"}, status=status.HTTP_400_BAD_REQUEST)  # 搜索信息为空的情况在前端已被拦
        cursor.execute(sql)
        for tup in cursor.fetchall():
            data.append({"id": tup[0], "name": tup[1], "content": tup[2], "year": tup[3], "college_name": tup[4],
                         "major_name": tup[5], "grade_number": tup[6], "grade_id": tup[7]})
        return Response({'student': data})
