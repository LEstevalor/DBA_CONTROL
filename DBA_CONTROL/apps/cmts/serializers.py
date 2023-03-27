from rest_framework import serializers

from cmts.models import College, Major, Teacher, Student


class CollegeSerializer(serializers.ModelSerializer):
    """学院信息序列化器"""
    id = serializers.IntegerField(label='id', read_only=True)  # 前端添加时需要返回id，给不刷新时的update和delete用

    class Meta:
        model = College
        fields = ['id', 'name', 'dean_id', 'content']


class MajorSerializer(serializers.ModelSerializer):
    """专业信息序列化器"""
    id = serializers.IntegerField(label='id', read_only=True)

    class Meta:
        model = Major
        fields = ['id', 'name', 'college_id', 'content']


class TeacherSerializer(serializers.ModelSerializer):
    """教师信息序列化器"""
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'college_id', 'content']


class StudentSerializer(serializers.ModelSerializer):
    """学生信息序列化器"""
    class Meta:
        model = Student
        fields = ['id', 'name', 'grade_id', 'content']
