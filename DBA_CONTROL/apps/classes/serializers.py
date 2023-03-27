from rest_framework import serializers

from classes.models import Teach_research_office, Grade


class TeachStudentClassSerializer(serializers.ModelSerializer):
    """教研室信息序列化器"""
    id = serializers.IntegerField(label='id', read_only=True)  # 前端添加时需要返回id，给不刷新时的update和delete用

    class Meta:
        model = Teach_research_office
        fields = ['id', 'college_id', 'count', 'location', 'content']


class GradeSerializer(serializers.ModelSerializer):
    """班级信息序列化器"""
    id = serializers.IntegerField(label='id', read_only=True)  # 前端添加时需要返回id，给不刷新时的update和delete用

    class Meta:
        model = Grade
        fields = ['id', 'grade_number', 'college_id', 'major_id', 'year', 'teach_id', 'count', 'content']
