from django.db import connection, transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from DBA_CONTROL.utils.tools import check_teach_name_and_id
from courses.models import Course, Student_Course
from courses.serializers import CourseSerializer, StudentCourseSerializer


class CoursesViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    """课程信息增删改查 模糊查
    list: 展示课程ID（id）、课程名称(name)、课程老师(teacher_name)、课程简介(content)、list(课程学生)  传的时候带教师ID，因教师名可能重复
    destory: 获取到课程ID后，删student_course和course
    update：课程ID存在，老师存在
    create: 课程ID存在，老师存在
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
        data = []
        for tup in cursor.fetchall():
            data.append({"id": tup[0], "name": tup[1], "teach_id": tup[2],
                         "teacher_name": tup[3], "content": tup[4]})
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
        teacher_name = check_teach_name_and_id(cursor, request.data['teacher_id'])
        # student是与course_id绑定的，而course_id是不可变的
        # SQL: update gdut_course set name=name, content=content, teach_id=teach_id where id=id
        super().update(self, request, *args, **kwargs)
        return Response({'teacher_name': teacher_name}, status=status.HTTP_200_OK)

    # POST /courses/  {id name content teach_id}
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        cursor = connection.cursor()
        teacher_name = check_teach_name_and_id(cursor, request.data['teacher_id'])  # 课程创建初始list为零，页面会提供增加功能
        # SQL: insert into gdut_course values(id, name, content, teach_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = dict(serializer.data)
        data["teacher_name"] = teacher_name
        return Response(data, status=status.HTTP_201_CREATED)  # super().create? create必须返回data，否则报错

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
        elif 'teach_id' in request.GET:
            sql = sql + " and t.id like '%s'" % ('%' + request.GET.get('id') + '%')
        elif 'student_id' in request.GET:
            sql = "select distinct(c.id), c.name, t.id, t.name, c.content from gdut_course c, gdut_teacher t, " \
                  "gdut_student_course sc where c.teacher_id = t.id and c.id = sc.course_id and sc.student_id like " \
                  "'%s'" % ('%' + request.GET.get('student_id') + '%')
        else:
            return Response({"message": "搜索信息有误"}, status=status.HTTP_400_BAD_REQUEST)  # 搜索信息为空的情况在前端已被拦

        cursor.execute(sql)
        tuples = cursor.fetchall()
        data = []
        for tup in tuples:
            data.append({"id": tup[0], "name": tup[1], "teach_id": tup[2],
                         "teacher_name": tup[3], "content": tup[4]})
        return Response({'courses': data})


class StudentCourseViewSet(CreateModelMixin, GenericViewSet):
    """ 学生课程视图
    student: 根据course_id获取上课人数
    add_student: 根据course_id，学号student_id加入课程，查看是否存在
    remove_student：根据course_id，学号student_id加入课程，查看是否不存在
    """
    permission_classes = [IsAuthenticated]
    serializer_class = StudentCourseSerializer

    def get_queryset(self):
        # select * from gdut_student_course
        return Student_Course.objects.all()

    # POST /student_course/  {course_id student_id}
    def create(self, request, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute("select id from gdut_student_course where course_id = '%s' and student_id = '%s'"
                       % (request.data['course_id'], request.data['student_id']))
        if cursor.fetchone() is not None:
            return Response({'message': '已存在'}, status=status.HTTP_400_BAD_REQUEST)

        cursor.execute("select name from gdut_student where id = '%s'" % request.data['student_id'])
        if cursor.fetchone() is None:
            return Response({'message': '学号不存在'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # GET /student_course/delete/  DELETE需要pk對應
    @action(methods=['get'], detail=False)
    def delete(self, request, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute("select id from gdut_student_course where course_id = '%s' and student_id = '%s'"
                       % (request.GET.get('course_id'), request.GET.get('student_id')))
        tup = cursor.fetchone()
        if tup is None:
            return Response({'message': '已不存在'}, status=status.HTTP_400_BAD_REQUEST)
        # delete gdut_student_course where id = id
        Student_Course.objects.filter(id=tup[0]).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # GET /student_course/student/?id=xxx
    @action(methods=['get'], detail=False)
    def student(self, request):
        cursor = connection.cursor()
        cursor.execute("select distinct(s.id), s.name from gdut_course c, gdut_student_course sc, gdut_student s  "
                       "where sc.course_id = '%s' and sc.student_id = s.id" % request.GET.get('id'))
        list_ = ''
        for tup_ in cursor.fetchall():
            list_ = list_ + tup_[0] + ' ' + tup_[1] + ' '
        return Response({'list': list_}, status=status.HTTP_200_OK)
