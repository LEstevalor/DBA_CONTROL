from rest_framework import serializers

from courses.models import Course, Student_Course


class CourseSerializer(serializers.ModelSerializer):
    """课程信息序列化器"""
    id = serializers.IntegerField(label='id', read_only=True)  # 前端添加时需要返回id，给不刷新时的update和delete用

    class Meta:
        model = Course
        fields = ['id', 'name', 'teacher_id', 'content']


class StudentCourseSerializer(serializers.ModelSerializer):
    """学生课程信息序列化器"""
    id = serializers.IntegerField(label='id', read_only=True)  # 前端添加时需要返回id，给不刷新时的update和delete用

    class Meta:
        model = Student_Course
        fields = ['id', 'course_id', 'student_id']
