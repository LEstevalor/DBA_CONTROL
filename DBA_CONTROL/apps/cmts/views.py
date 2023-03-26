from django.db import connection
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from classes.models import Grade
from cmts.models import College, Teacher, Major
from cmts.serializers import CollegeSerializer, MajorSerializer


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
        if 'college_name' in request.GET:
            college_name = '%' + request.GET.get('college_name') + '%'  # 需要%s为'%s'，否则识别不出来
            cursor.execute("select c.id, c.name, t.name, c.content from gdut_college c, gdut_teacher t where c.dean_id = t.id and c.name like '%s'" % college_name)
        elif 'dean_name' in request.GET:
            dean_name = '%' + request.GET.get('dean_name') + '%'
            cursor.execute("select c.id, c.name, t.name, c.content from gdut_college c, gdut_teacher t where c.dean_id = t.id and t.name like '%s'" % dean_name)
        elif 'content' in request.GET:
            content = '%' + request.GET.get('content') + '%'
            cursor.execute("select c.id, c.name, t.name, c.content from gdut_college c, gdut_teacher t where c.dean_id = t.id and c.content like '%s'" % content)
        else:
            return Response({"message": "搜索信息有误"}, status=status.HTTP_400_BAD_REQUEST)  # 搜索信息为空的情况在前端已被拦
        tuples = cursor.fetchall()
        for tup in tuples:
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
            cursor.execute("select count(*) from gdut_grade where gdut_grade.major_id = '%s'", tup[0])
            count = cursor.fetchone()[0]
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
