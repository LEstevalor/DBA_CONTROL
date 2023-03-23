import re

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from cmts.models import Student, Teacher
from user.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """注册序列化器"""
    password2 = serializers.CharField(label='确认密码', write_only=True)  # 只有password2是User模型中没有的，只写
    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'mobile', 'email', 'level', 'token']
        # 不需要验证码，已写在EmailVerifyView的POST方法中

    # def validate_level(self, attrs):
    #     """根据账户赋予权限"""
    #     username = attrs["username"]
    #     if Student.objects.filter(id=username).count() == 1:
    #         return 'USER'
    #     elif Teacher.objects.filter(id=username).count() == 1:
    #         return 'ADMIN'
    #     elif username == 'admin':
    #         return 'SUPER_ADMIN'
    #     raise serializers.ValidationError('不存在该账号，请联系管理员')
    #
    # def validate_mobile(self, value):
    #     """单独校验手机号"""
    #     if not re.match(r'1[3-9]\d{9}$', value):
    #         print(value)
    #         print(re.match(r'1[3-9]\d{9}$', value))
    #         print(re.match(r'1[3-9]\d{9}$', str(value)))
    #         raise serializers.ValidationError('手机号格式有误')
    #     return value

    def validate(self, attrs):
        """校验两个密码是否相同 与 校验手机号"""
        for i in attrs:
            print(i)

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两个密码不一致')

        if not re.match(r'1[3-9]\d{9}$', attrs['mobile']):
            raise serializers.ValidationError('手机号格式有误')

        username = attrs["username"]
        if Student.objects.filter(id=username).count() == 1:
            attrs["level"] = 'USER'
        elif Teacher.objects.filter(id=username).count() == 1:
            attrs["level"] = 'ADMIN'
        elif username == 'admin':
            attrs["level"] = 'SUPER_ADMIN'
        else:
            raise serializers.ValidationError('不存在该账号，请联系管理员')

        return attrs


    def create(self, validated_data):
        del validated_data['password2']  # 入库并不需要该字段

        user = User(**validated_data)  # 创建User（下面还得存到数据库中）
        # password = validated_data.pop('password')
        # user.set_password(password)  # 这里可以搞密码入库加密
        # insert into users values(id, username, password, mobile, email)
        user.save()  # 存到数据库

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 引用JWT的jwt_encode_handler函数（用于生成jwt）
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)  # 根据user生成payload载荷
        token = jwt_encode_handler(payload)  # 如果配置文件有SECRET_KEY，就只需传载荷，就能生成JWT
        user.token = token  # 赋给token给前端

        return user


class MyTokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        data['token'] = data['access']
        data['username'] = self.user.username
        return data
