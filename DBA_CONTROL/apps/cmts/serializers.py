from rest_framework import serializers

from cmts.models import College


class CollegeSerializer(serializers.ModelSerializer):
    """学院信息序列化器"""
    class Meta:
        model = College
        fields = ['name', 'dean_id', 'content']
