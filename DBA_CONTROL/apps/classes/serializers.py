from rest_framework import serializers

from classes.models import Teach_research_office


class TeachStudentClassSerializer(serializers.ModelSerializer):
    """学院信息序列化器"""
    id = serializers.IntegerField(label='id', read_only=True)  # 前端添加时需要返回id，给不刷新时的update和delete用

    class Meta:
        model = Teach_research_office
        fields = ['id', 'college_id', 'count', 'location', 'content']
