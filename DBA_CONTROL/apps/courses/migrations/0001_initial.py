# Generated by Django 3.2.18 on 2023-03-23 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='课程ID')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('teacher_id', models.CharField(max_length=20, verbose_name='教师ID')),
                ('content', models.TextField(blank=True, max_length=256, verbose_name='备注')),
            ],
            options={
                'verbose_name': '课程',
                'verbose_name_plural': '课程',
                'db_table': 'gdut_course',
            },
        ),
        migrations.CreateModel(
            name='Student_Course',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=20, verbose_name='课程ID')),
                ('student_id', models.CharField(max_length=20, verbose_name='学号')),
            ],
            options={
                'verbose_name': '学生课程',
                'verbose_name_plural': '学生课程',
                'db_table': 'gdut_student_course',
            },
        ),
    ]