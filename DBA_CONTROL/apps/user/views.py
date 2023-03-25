import logging

from django.db import connection
from django.conf import settings
from random import randint
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from DBA_CONTROL.utils import constants
from DBA_CONTROL.utils.tools import is_valid_email
from cmts.models import Student, Teacher
from user.models import User
from user.serializers import CreateUserSerializer, MyTokenObtainPairSerializer, UserDetailSerializer

logger = logging.getLogger('django')


class EmailSendView(APIView):
    """通过用户邮箱，发送验证码，有效期为5分钟，存入非关系型数据库redis中"""

    def get(self, request):
        email = request.GET.get("email")
        if not is_valid_email(email):
            return Response({'message': '邮箱格式不合法'}, status=status.HTTP_400_BAD_REQUEST)

        redis_conn = get_redis_connection('verify_codes')
        sms_code = "%06d" % randint(0, 999999)  # 自定义生成六位验证码
        send_flag = redis_conn.get('send_flag_%s' % email)
        if send_flag:
            return Response({'message': '频繁发送邮箱申请验证码'}, status=status.HTTP_400_BAD_REQUEST)

        print(sms_code)  # 生成环境中不留该类测试数据
        logger.info(sms_code)

        pl = redis_conn.pipeline()  # redis管道技术
        pl.setex('send_%s' % email, constants.USER_EMAIL_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % email, constants.USER_SEND_SMS_CODE_INTERVAL, 1)
        pl.execute()

        subject = "GDUT DBA系统 邮箱验证"
        html_message = '<p>尊敬的⽤户您好！只因你！</p>' \
                       '<p>感谢您使⽤GDUT DBA系统。</p>' \
                       '<p>您的邮箱为：%s ，验证码为：%s</p>' % (email, sms_code)
        send_mail(subject, "", settings.EMAIL_FROM, [email], html_message=html_message)

        return Response({'message': 'ok'})


class EmailVerifyView(APIView):
    """邮箱验证码验证"""
    def get(self, request):
        # post请求 print(request.data)  # 测试数据：{'sms_code': 123456}
        front_email_code = request.GET.get("sms_code")  # 前端提交的验证码
        redis_conn = get_redis_connection('verify_codes')
        real_email_code = redis_conn.get('send_%s' % request.GET.get("email")).decode('UTF-8')
        # b'xxxxxx' bytes类型，需转成字符串，如果先转成int那么避免不了前面为0的情况，012345 -》 12345，字节型变字符串用bytes.decode('UTF-8')

        if real_email_code is None:  # 验证码过期的情况
            return Response({'message': '验证码过期或未申请过'}, status=status.HTTP_400_BAD_REQUEST)
        if front_email_code != real_email_code:
            return Response({'message': '验证码错误'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'ok'}, status=status.HTTP_200_OK)


class UniqueView(APIView):
    """唯一注册视图"""
    def get(self, request):
        str = request.GET.get("str")
        front_str = request.GET.get(str)
        if str == "username":  # 检查是否有重复的账号
            # SQL: select count(*) from user where username = front_str
            count = User.objects.filter(username=front_str).count()
        else:  # 检查是否有重复的邮箱
            # SQL: select count(*) from user where email = front_str
            count = User.objects.filter(email=front_str).count()

        return Response({"count": count})


class RegisterUserView(CreateAPIView):
    """用户注册视图"""
    serializer_class = CreateUserSerializer


class LoginTokenView(TokenViewBase):
    """ jwt登录视图 按照TokenObtainPairView重写为自己调用的视图"""
    serializer_class = MyTokenObtainPairSerializer


class RealNameView(APIView):
    """用户信息视图"""
    def get(self, request):
        username = request.GET.get("username")
        cursor = connection.cursor()  # 连接数据库对象

        # select * from student where id = username
        # student = Student.objects.filter(id=username)  # 拿出的是QuerySet，返回前端好用，或者value_list(value)拿到的也是queryset
        cursor.execute("SELECT name FROM gdut_student WHERE id = %s" % username)
        student_name = cursor.fetchone()
        if student_name is not None:
            return Response({"username_realname": (student_name[0] + "同学")})

        # select * from teacher where id = username
        # teacher = Teacher.objects.filter(id=username)
        cursor.execute("SELECT name FROM gdut_teacher WHERE id = %s" % username)
        teacher_name = cursor.fetchone()
        if teacher_name is not None:
            return Response({"username_realname": (teacher_name[0] + "老师")})
        return Response({'message': 'username错误'}, status=status.HTTP_400_BAD_REQUEST)


class UserView(RetrieveAPIView):
    """⽤户登录信息鉴定"""
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    # 重写get_object方法返回给前端字段，否则会报queryset的错误
    def get_object(self):
        return self.request.user


class StatusView(APIView):
    """权限获取视图"""
    def get(self, request):
        username = request.GET.get("username")
        cursor = connection.cursor()  # 连接数据库对象
        # select level from gdut_users where username = username  字符串这里需要加''在数据库中，'admin'或3120006969生效（数字可不需）
        cursor.execute("SELECT level FROM gdut_users WHERE username = '%s'" % username)
        level = cursor.fetchone()
        if level is not None:
            return Response({"status": level[0]})
        else:
            return Response({'message': '搜取不到权限'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
