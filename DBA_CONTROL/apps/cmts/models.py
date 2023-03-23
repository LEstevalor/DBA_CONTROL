from django.db import models

from DBA_CONTROL.utils.models import BaseModel
from classes.models import Grade


class Student(BaseModel):
    """学生模型类"""
    """ SQL: 
    create table Student(
        id CHAR(20) PRIMARY KEY COMMENT '学号',
        name CHAR(20) NOT NULL COMMENT '姓名',
        grade_id CHAR(20) NOT NULL COMMENT '班级ID',
        content VARCHAR(256) COMMENT '备注'
    ) COMMENT='学生';
    """
    id = models.CharField(primary_key=True, max_length=20, verbose_name='学号')
    name = models.CharField(max_length=20, verbose_name='姓名')
    grade_id = models.CharField(max_length=20, verbose_name='班级ID')
    content = models.TextField(max_length=256, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'gdut_student'
        verbose_name = '学生'
        verbose_name_plural = verbose_name


class Teacher(BaseModel):
    """教师模型类"""
    """ SQL: 
    create table Teacher(
        id CHAR(20) PRIMARY KEY COMMENT '教师号',
        name CHAR(20) NOT NULL COMMENT '姓名',
        college_id CHAR(20) NOT NULL COMMENT '学院ID',
        content VARCHAR(256) COMMENT '备注'
    ) COMMENT='教师';
    """
    id = models.CharField(primary_key=True, max_length=20, verbose_name='教师号')
    name = models.CharField(max_length=20, verbose_name='姓名')
    college_id = models.CharField(max_length=20, verbose_name='学院ID')
    content = models.TextField(max_length=256, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'gdut_teacher'
        verbose_name = '教师'
        verbose_name_plural = verbose_name


class College(BaseModel):
    """学院模型类"""
    """ SQL: 
    create table College(
        id CHAR(20) PRIMARY KEY COMMENT '学院ID',
        name CHAR(50) UNIQUE NOT NULL COMMENT '学院名',
        dean_id CHAR(20) NOT NULL COMMENT '院长ID',
        content VARCHAR(256) COMMENT '备注'
    ) COMMENT='学院';
    """
    id = models.CharField(primary_key=True, max_length=20, verbose_name='学院ID')
    name = models.CharField(max_length=50, unique=True,verbose_name='学院名')
    dean_id = models.CharField(max_length=20, verbose_name='院长ID')
    content = models.TextField(max_length=256, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'gdut_college'
        verbose_name = '学院'
        verbose_name_plural = verbose_name


class Major(BaseModel):
    """专业模型类"""
    """ SQL: 
    create table Major(
        id CHAR(20) PRIMARY KEY COMMENT '专业ID',
        name CHAR(50) NOT NULL COMMENT '专业名称',
        college_id CHAR(20) NOT NULL COMMENT '学院ID',
        content VARCHAR(256) COMMENT '备注'
    ) COMMENT='专业';
    """
    id = models.CharField(primary_key=True, max_length=20, verbose_name='专业ID')
    name = models.CharField(max_length=50, verbose_name='专业名称')
    college_id = models.CharField(max_length=20, verbose_name='学院ID')
    content = models.TextField(max_length=256, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'gdut_major'
        verbose_name = '专业'
        verbose_name_plural = verbose_name
