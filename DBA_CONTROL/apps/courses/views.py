from django.db import connection
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from DBA_CONTROL.utils.tools import check_teach_name_and_id
from courses.models import Course, Student_Course
from courses.serializers import CourseSerializer


class CoursesViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    """课程信息增删改查 模糊查
    list: 展示课程ID（id）、课程名称(name)、课程老师(teacher_name)、课程简介(content)、list(课程学生)  传的时候带教师ID，因教师名可能重复
    destory: 获取到课程ID后，删student_course和course
    update：课程ID存在，老师存在（用另一个视图对改list）
    create: 课程ID存在，老师存在（用另一个视图对改list）
    search: 课程名、老师名、简介、学生（查学生时，调用student_class）
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def get_queryset(self):
        # select * from gdut_course
        return Course.objects.all()

    # GET /courses/
    def list(self, request, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute("select c.id, c.name, t.id, t.name, c.content from gdut_course c, gdut_teacher t where c.teacher_id = t.id")
        tuples = cursor.fetchall()
        data = []
        for tup in tuples:
            cursor.execute("select s.id, s.name from gdut_course c, gdut_student_course sc, gdut_student s  "
                           "where sc.course_id = c.id and sc.student_id = s.id")
            list_ = ''
            for tup_ in cursor.fetchall():
                list_ = list_ + tup_[0] + ' ' + tup_[1] + ' '
            data.append({"id": tup[0], "name": tup[1], "teach_id": tup[2],
                         "teacher_name": tup[3], "content": tup[4], "list": list_})
        return Response({'courses': data})

    # DELETE /courses/<pk>/
    def destroy(self, request, *args, **kwargs):
        # delete from gdut_student_course where course_id = pk
        Student_Course.objects.filter(course_id=kwargs.pk).delete()
        super().destroy(self, request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)  # 即使父类方法有但仍需补充Response，否则报错

    # PUT /courses/<pk>/JSON内容  {name, content, teach_id}
    def update(self, request, *args, **kwargs):
        cursor = connection.cursor()
        check_teach_name_and_id(cursor, request.data['teach_id'])
        # student是与course_id绑定的，而course_id是不可变的
        # SQL: update gdut_course set name=name, content=content, teach_id=teach_id where id=id
        super().update(self, request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)

    # POST /courses/  {id name content teach_id}
    def create(self, request, *args, **kwargs):
        cursor = connection.cursor()
        check_teach_name_and_id(cursor, request.data['teach_id'])  # 课程创建初始list为零，页面会提供增加功能
        # SQL: insert into gdut_course values(id, name, content, teach_id)
        super().create(self, request, *args, **kwargs)
        return Response(status=status.HTTP_201_CREATED)

    # GET /courses/search/?xxx 模糊查询
    @action(methods=['get'], detail=False)
    def search(self, request):
        cursor = connection.cursor()
        sql = "select c.id, c.name, t.id, t.name, c.content from gdut_course c, gdut_teacher t where c.teacher_id = t.id"
        if 'name' in request.GET:
            sql = sql + " and c.name like %s" % ('%' + request.GET.get('content') + '%')
        elif 'content' in request.GET:
            sql = sql + " and c.content like '%s'" % ('%' + request.GET.get('content') + '%')
        elif 'teacher_name' in request.GET:
            sql = sql + " and t.name like '%s'" % ('%' + request.GET.get('teacher_name') + '%')
        else:
            return Response({"message": "搜索信息有误"}, status=status.HTTP_400_BAD_REQUEST)  # 搜索信息为空的情况在前端已被拦

        cursor.execute(sql)
        tuples = cursor.fetchall()
        data = []
        for tup in tuples:
            cursor.execute("select s.id, s.name from gdut_course c, gdut_student_course sc, gdut_student s  "
                           "where sc.course_id = c.id and sc.student_id = s.id")
            list_ = ''
            for tup_ in cursor.fetchall():
                list_ = list_ + tup_[0] + ' ' + tup_[1] + ' '
            data.append({"id": tup[0], "name": tup[1], "teach_id": tup[2],
                         "teacher_name": tup[3], "content": tup[4], "list": list_})
        return Response({'courses': data})
