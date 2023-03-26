from django.db import models

from DBA_CONTROL.utils.models import BaseModel


class Grade(BaseModel):
    """班级模型类"""
    """ SQL: 
    create table Grade(
        id SMALLINT PRIMARY KEY AUTO_INCREMENT COMMENT '班级ID',  -- django中未创建会生成自动的默认自增ID
        grade_number SMALLINT NOT NULL COMMENT '班级号',
        college_id CHAR(20) NOT NULL COMMENT '学院ID',
        major_id CHAR(20) NOT NULL COMMENT '专业ID',
        year SMALLINT NOT NULL COMMENT '届号',
        teach_id CHAR(20) NOT NULL COMMENT '班主任ID',
        count SMALLINT NOT NULL COMMENT '人数',
        content VARCHAR(256) COMMENT '备注'
    ) COMMENT='班级';
    """
    grade_number = models.IntegerField(verbose_name='班级号')
    college_id = models.CharField(max_length=20, verbose_name='学院ID')
    major_id = models.CharField(max_length=20, verbose_name='专业ID')
    year = models.IntegerField(verbose_name='届号')
    teach_id = models.CharField(max_length=20, verbose_name='班主任ID')
    count = models.IntegerField(verbose_name='人数')
    content = models.TextField(max_length=256, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'gdut_grade'
        verbose_name = '班级'
        verbose_name_plural = verbose_name


class Teach_research_office(BaseModel):
    """教研室模型类"""
    """ SQL: 
    create table Teach_research_office(
        id SMALLINT PRIMARY KEY AUTO_INCREMENT COMMENT '教研室ID',  -- django中未创建会生成自动的默认自增ID
        college_id CHAR(20) NOT NULL COMMENT '学院ID',
        count SMALLINT NOT NULL COMMENT '可容纳人数',
        location VARCHAR(256) UNIQUE NOT NULL COMMENT '地理位置'
        content VARCHAR(256) COMMENT '备注'
    ) COMMENT='教研室';
    """
    college_id = models.CharField(max_length=20, verbose_name='学院ID')
    count = models.IntegerField(verbose_name='可容纳人数')
    location = models.CharField(max_length=100, unique=True, verbose_name='地理位置')
    # 官网：because unique implies the creation of an index.
    content = models.TextField(max_length=256, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'gdut_teach_research_office'
        verbose_name = '教研室'
        verbose_name_plural = verbose_name
