from django.contrib.auth.models import AbstractUser
from django.db import models

from DBA_CONTROL.utils.models import BaseModel


class User(BaseModel):
    """自定义用户模型类"""
    # 账号 密码 电话 邮箱 用户级别
    userid = models.CharField(max_length=20, unique=True, verbose_name='账号')
    password = models.CharField(max_length=20, verbose_name='密码')
    mobile = models.CharField(max_length=11, blank=True, verbose_name='手机号')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    level = (
        ("USER", "普通用户"),
        ("ADMIN", "管理员"),
        ("SUPER_ADMIN", "超级管理员")
    )

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        # 元数据主要用在管理后台的展示上，verbose_name_plural 是模型类的复数名 。如果不设置的话，Django 会使用小写的模型名作为默认值，并且在结尾加上 s。通过此项元数据设置名字可以去掉 s。
