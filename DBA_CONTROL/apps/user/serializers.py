import re

from rest_framework import serializers

from user.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """注册序列化器"""
    password2 = serializers.CharField(label='确认密码', write_only=True)  # 只有password2是User模型中没有的，只写

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'mobile', 'email', 'level']
        # 不需要验证码，已写在EmailVerifyView的POST方法中

    def validate_level(self, value):
        """根据账户赋予权限"""
        pass

    def validate_mobile(self, value):
        """单独校验手机号"""
        if not re.match(r'1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式有误')
        return value

    def validate(self, attrs):
        """校验两个密码是否相同 与 校验密码"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两个密码不一致')

    def create(self, validated_data):
        del validated_data['password2']  # 入库并不需要该字段

        user = User(**validated_data)  # 创建User（下面还得存到数据库中）
        # password = validated_data.pop('password')
        # user.set_password(password)  # 这里可以搞一个加密
        user.save()  # 存到数据库
        return user
