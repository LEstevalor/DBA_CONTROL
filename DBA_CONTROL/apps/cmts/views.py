from django.db import connection
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from cmts.models import College, Teacher
from cmts.serializers import CollegeSerializer


class CollegeViewSet(DestroyModelMixin, GenericViewSet):
    """学院信息增删改查 模糊查"""
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
