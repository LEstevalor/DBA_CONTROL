# Generated by Django 3.2.18 on 2023-03-26 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20230326_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_course',
            name='course_id',
            field=models.IntegerField(verbose_name='课程ID'),
        ),
    ]