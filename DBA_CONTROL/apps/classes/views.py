from django.db import connection
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from classes.models import Teach_research_office
from classes.serializers import TeachStudentClassSerializer


def check_college_name(cursor, college_name):
    """传入connection和学院name，检查学院名称是否存在，如果存在则返回学院ID，不存在则报错404"""
    cursor.execute("select id from gdut_college where name = '%s'" % college_name)
    tuple_info = cursor.fetchone()
    # select count(*) from gdut_college where name = college_name;
    if tuple_info is None:
        return Response({"message": "学院不存在"}, status=status.HTTP_400_BAD_REQUEST)
    return tuple_info[0]


class TeachStudentClassViewSet(GenericViewSet):
    """教研室信息增删改查 模糊查"""
    permission_classes = [IsAuthenticated]
    serializer_class = TeachStudentClassSerializer

    def get_queryset(self):
        # select * from Teach_research_office
        return Teach_research_office.objects.all()

    # GET /teach_student_class/
    def list(self, request, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute("select c.name, t.location, t.count, t.content, t.id from gdut_college c, gdut_teach_research_office t where c.id = t.college_id")
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
            count = request.GET.get('count')
            sql = "select c.name, t.location, t.count, t.content, t.id from gdut_college c, gdut_teach_research_office t where c.id = t.college_id and t.count >= %s" % count
        else:
            return Response({"message": "搜索信息有误"}, status=status.HTTP_400_BAD_REQUEST)  # 搜索信息为空的情况在前端已被拦
        cursor.execute(sql)
        for tup in cursor.fetchall():
            data.append({"ip": tup[0], "source": tup[1], "count": tup[2], "content": tup[3], "id": tup[4]})
        return Response({'teach_student_class': data})
