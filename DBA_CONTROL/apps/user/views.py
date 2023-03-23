import logging

from django.conf import settings
from random import randint
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework.response import Response

from DBA_CONTROL.utils import constants
from DBA_CONTROL.utils.tools import is_valid_email

logger = logging.getLogger('django')


class EmailVerifyView(APIView):
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
