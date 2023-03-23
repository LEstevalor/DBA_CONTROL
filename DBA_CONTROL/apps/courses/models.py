from django.db import models

from DBA_CONTROL.utils.models import BaseModel


class Course(BaseModel):
    """课程模型类"""
    """ SQL: 
    create table Course(
        id CHAR(20) PRIMARY KEY COMMENT '课程ID',
        name CHAR(20) NOT NULL COMMENT '课程名',
        teacher_id CHAR(20) NOT NULL COMMENT '教师ID',
        content VARCHAR(256) COMMENT '备注'
    ) COMMENT='课程';
    """
    id = models.CharField(primary_key=True, max_length=20, verbose_name='课程ID')
    name = models.CharField(max_length=20, verbose_name='姓名')
    teacher_id = models.CharField(max_length=20, verbose_name='教师ID')
    content = models.TextField(max_length=256, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'gdut_course'
        verbose_name = '课程'
        verbose_name_plural = verbose_name


class Student_Course(BaseModel):
    """学生课程模型类"""
    """ SQL: 
    create table Student_Course(
        id CHAR(20) PRIMARY KEY COMMENT 'ID',
        course_id CHAR(20) NOT NULL COMMENT '课程ID',
        student_id CHAR(20) NOT NULL COMMENT '学号'
    ) COMMENT='学生课程';
    """
    id = models.CharField(primary_key=True, max_length=20, verbose_name='ID')
    course_id = models.CharField(max_length=20, verbose_name='课程ID')
    student_id = models.CharField(max_length=20, verbose_name='学号')

    class Meta:
        db_table = 'gdut_student_course'
        verbose_name = '学生课程'
        verbose_name_plural = verbose_name