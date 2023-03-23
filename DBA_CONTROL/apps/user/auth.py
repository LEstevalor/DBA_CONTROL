import re
from django.contrib.auth.backends import ModelBackend

from .models import User


def get_user_by_account(account):
    """根据传⼊的账号获取⽤户信息"""
    try:
        if re.match('^1[3-9]\d{9}$', account):
            # ⼿机号登录
            user = User.objects.get(email=account)
        else:
            # ⽤户名登录
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class MyAuthBackend(ModelBackend):
    """修改⽤户认证系统的后端，⽀持多账号登录"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 根据传⼊的username获取user对象。username可以是邮箱也可以是账号
        user = get_user_by_account(username)
        # 校验user是否存在并校验密码是否正确
        if user:
            return user
