from django.db import connection
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from DBA_CONTROL.utils.tools import check_teach_name_and_id
from classes.models import Teach_research_office, Grade
from classes.serializers import TeachStudentClassSerializer, GradeSerializer


def check_college_name(cursor, college_name):
    """传入connection和学院name，检查学院名称是否存在，如果存在则返回学院ID，不存在则报错404"""
    cursor.execute("select id from gdut_college where name = '%s'" % college_name)
    tuple_info = cursor.fetchone()
    if tuple_info is None:
        return Response({"message": "学院不存在"}, status=status.HTTP_400_BAD_REQUEST)
    return tuple_info[0]


def check_major_name(cursor, major_name):
    """传入connection和专业name，检查专业名称存在否，如果存在则返回major.id，不存在则报错404"""
    cursor.execute("select id from gdut_major where name = '%s'" % major_name)
    tuple_info = cursor.fetchone()
    if tuple_info is None:
        return Response({"message": "专业不存在"}, status=status.HTTP_400_BAD_REQUEST)
    return tuple_info[0]


def check_same_grade(cursor, year, college_id, major_id, grade_number):
    """检查是否有同届同学院同专业同班号的情况发生，无则不返回，存在则报错"""
    cursor.execute("select content from gdut_grade where year = %s and college_id = '%s' and major_id = '%s' and "
                   "grade_number = %s " % (year, college_id, major_id, grade_number))
    if cursor.fetchone() is None:
        return Response({"message": "教师ID不存在或教师名称与教师ID匹配不上"}, status=status.HTTP_400_BAD_REQUEST)


class TeachStudentClassViewSet(DestroyModelMixin, GenericViewSet):
    """教研室信息增删改查 模糊查"""
    permission_classes = [IsAuthenticated]
    serializer_class = TeachStudentClassSerializer

    def get_queryset(self):
        # select * from Teach_research_office
        return Teach_research_office.objects.all()

    # GET /teach_student_class/
    def list(self, request, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute(
            "select c.name, t.location, t.count, t.content, t.id from gdut_college c, gdut_teach_research_office t where c.id = t.college_id")
        tuples = cursor.fetchall()
        data = []
        for tup in tuples:
            data.append({"ip": tup[0], "source": tup[1], "count": tup[2], "content": tup[3], "id": tup[4]})

        return Response({'teach_student_class': data})

    # DELETE /teach_student_class/<pk>/
    # destroy交给DestroyModelMixin了，但注意前端传入必须为ID（pk字段才匹配得上）

    # PUT /teach_student_class/<pk>/JSON内容
    # 除地理位置location不可变，传入college_name content count是可变的
    # 学院需存在，count为正整数
    def update(self, request, *args, **kwargs):
        if int(request.data["count"]) < 0:
            return Response({"message": "容纳人数需大于等于0"}, status=status.HTTP_400_BAD_REQUEST)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        cursor = connection.cursor()
        request.data['college_id'] = check_college_name(cursor, request.data["college_name"])
        request.data.pop("college_name")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # update gdut_teach_research_office set college_id = college_id, content = content, count = count where id = id
        serializer.save()
        return Response(serializer.data)

    # POST /teach_student_class/
    # POST请求方式，数据为全新新增的，故不需要带*args, **kwargs
    # 传入college_name location content count
    def create(self, request):
        if int(request.data["count"]) < 0:
            return Response({"message": "容纳人数需大于等于0"}, status=status.HTTP_400_BAD_REQUEST)
        cursor = connection.cursor()
        request.data['college_id'] = check_college_name(cursor, request.data["college_name"])

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
            sql = "select c.name, t.location, t.count, t.content, t.id from gdut_college c, gdut_teach_research_office t where c.id = t.college_id and c.name like '%s'" % college_name
        elif 'location' in request.GET:
            location = '%' + request.GET.get('location') + '%'
            sql = "select c.name, t.location, t.count, t.content, t.id from gdut_college c, gdut_teach_research_office t where c.id = t.college_id and t.location like '%s'" % location
        elif 'content' in request.GET:
            content = '%' + request.GET.get('content') + '%'
            sql = "select c.name, t.location, t.count, t.content, t.id from gdut_college c, gdut_teach_research_office t where c.id = t.college_id and t.content like '%s'" % content
        elif 'count' in request.GET:
            count = str(int(request.GET.get('count')))  # 以防SQL注入
            sql = "select c.name, t.location, t.count, t.content, t.id from gdut_college c, gdut_teach_research_office t where c.id = t.college_id and t.count >= %s" % count
        else:
            return Response({"message": "搜索信息有误"}, status=status.HTTP_400_BAD_REQUEST)  # 搜索信息为空的情况在前端已被拦
        cursor.execute(sql)
        for tup in cursor.fetchall():
            data.append({"ip": tup[0], "source": tup[1], "count": tup[2], "content": tup[3], "id": tup[4]})
        return Response({'teach_student_class': data})


class GradeViewSet(DestroyModelMixin, GenericViewSet):
    """
    班级信息增删改查 模糊查
    list: 展示 届号（year）、学院名称(college_name)、专业名称(major_name)、班号（grade_number）、班主任（teacher_name）、
            班级人数（count）、班级简介（content）
            四表连接，grade college major teacher
    destory: 获取到班级ID后，需判断当前count是否为0，（删除时count已为0，major的人数不必要变化）
    update：需确保学院存在、专业存在、教师存在，id是不可update的，因此count的变化控制完全交给student，另外当改变专业时，
            由于专业人数是根据班级确定的，还需要修改对应专业的人数变化，与修改专业的人数变化，
            还要确保没有 同届同学院同专业同班号的情况发生
    create: 需确保学院存在、专业存在、教师存在，count初始传入为0（控制权随student变化），还要确保没有 同届同学院同专业同班号的情况发生
    search: 可以根据 届号（year）、学院名称(college_name)、专业名称(major_name)、班号（grade_number）、班主任（teacher_name）、
            班主任ID（teach_id）、班级人数（count）、班级简介（content）查询，count为大于等于查询，其他为模糊查
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GradeSerializer

    def get_queryset(self):
        # select * from gdut_grade
        return Grade.objects.all()

    # GET /grade/
    def list(self, request, *args, **kwargs):
        cursor = connection.cursor()
        sql = "select g.id, g.year, c.name, m.name, g.grade_number, t.id, t.name, g.count, g.content from " \
              "gdut_grade g, gdut_college c, gdut_major m, gdut_teacher t where g.college_id = c.id and " \
              "g.major_id = m.id and g.teach_id = t.id"  # 为什么要teach_id，因为教师的名字可能不唯一，用于create和update辨别
        cursor.execute(sql)
        tuples = cursor.fetchall()
        data = []
        for tup in tuples:
            data.append({"id": tup[0], "year": tup[1], "college_name": tup[2],
                         "major_name": tup[3], "grade_number": tup[4], "teach_id": tup[5],
                         "teacher_name": tup[6], "count": tup[7], "content": tup[8]})
        return Response({'grade': data})

    # DELETE /grade/<pk>/?count=0
    def destroy(self, request, *args, **kwargs):
        if int(request.GET.get("count")) != 0:
            return Response({"message": "删除班级的人数需为0"}, status=status.HTTP_400_BAD_REQUEST)
        super().destroy(self, request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)  # 即使父类方法有但仍需补充Response，否则报错

    # PUT /grade/<pk>/JSON内容
    def update(self, request, *args, **kwargs):
        # count是不可变的，因为count只与student绑定grade_id有关
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        cursor = connection.cursor()
        request.data['college_id'] = check_college_name(cursor, request.data["college_name"])
        request.data['major_id'] = check_major_name(cursor, request.data["major_name"])
        check_teach_name_and_id(cursor, request.data["teach_id"], request.data["teacher_name"])
        # request.data.pop("college_name") request.data.pop("major_name") request.data.pop("teacher_name")
        # request.data多余的可以不pop掉，只有序列化器有即可
        check_same_grade(cursor, request.data["year"], request.data["college_id"],
                         request.data["major_id"], request.data["grade_number"])

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # update gdut_teach set year=year, college_id=college_id, major_id=major_id, teach_id=teach_id,
        # content=content, count=count, grade_number=grade_number where id = id
        serializer.save()
        return Response(serializer.data)

    # POST /grade/
    # 传入 year grade_number college_name major_name teach_id teacher_name count content
    def create(self, request):
        if int(request.data["count"]) != 0:
            return Response({"message": "班级初始人数必须为0"}, status=status.HTTP_400_BAD_REQUEST)
        cursor = connection.cursor()
        request.data['college_id'] = check_college_name(cursor, request.data["college_name"])
        request.data['major_id'] = check_major_name(cursor, request.data["major_name"])
        check_teach_name_and_id(cursor, request.data["teach_id"], request.data["teacher_name"])
        check_same_grade(cursor, request.data["year"], request.data["college_id"],
                         request.data["major_id"], request.data["grade_number"])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # GET /grade/search/?xxx 模糊查询
    @action(methods=['get'], detail=False)
    def search(self, request):
        data = []
        cursor = connection.cursor()
        sql = "select g.id, g.year, c.name, m.name, g.grade_number, t.id, t.name, g.count, g.content from " \
              "gdut_grade g, gdut_college c, gdut_major m, gdut_teacher t where g.college_id = c.id and " \
              "g.major_id = m.id and g.teach_id = t.id"
        if 'id' in request.GET:
            sql = sql + " and g.id = %s" % str(int(request.GET.get('id')))
        elif 'year' in request.GET:
            sql = sql + " and g.year like %s" % ('%' + request.GET.get('year') + '%')
        elif 'college_name' in request.GET:
            sql = sql + " and c.name like '%s'" % ('%' + request.GET.get('college_name') + '%')
        elif 'major_name' in request.GET:
            sql = sql + " and m.name like '%s'" % ('%' + request.GET.get('major_name') + '%')
        elif 'grade_number' in request.GET:
            sql = sql + " and g.grade_number = %s" % str(int(request.GET.get('grade_number')))
        elif 'teacher_name' in request.GET:
            sql = sql + " and t.name like '%s'" % ('%' + request.GET.get('teacher_name') + '%')
        elif 'teach_id' in request.GET:
            sql = sql + " and t.id like '%s'" % ('%' + request.GET.get('teach_id') + '%')
        elif 'content' in request.GET:
            sql = sql + " and g.content like '%s'" % ('%' + request.GET.get('content') + '%')
        elif 'count' in request.GET:
            sql = " g.count >= %s" % str(int(request.GET.get('count')))  # 以防SQL注入
        else:
            return Response({"message": "搜索信息有误"}, status=status.HTTP_400_BAD_REQUEST)  # 搜索信息为空的情况在前端已被拦
        cursor.execute(sql)
        for tup in cursor.fetchall():
            data.append({"id": tup[0], "year": tup[1], "college_name": tup[2],
                         "major_name": tup[3], "grade_number": tup[4], "teach_id": tup[5],
                         "teacher_name": tup[6], "count": tup[7], "content": tup[8]})
        return Response({'grade': data})
