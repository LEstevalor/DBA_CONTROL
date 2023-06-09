# Generated by Django 3.2.18 on 2023-03-23 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='账号')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
                ('mobile', models.CharField(blank=True, max_length=11, verbose_name='手机号')),
                ('email', models.EmailField(max_length=30, unique=True, verbose_name='邮箱')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'gdut_users',
            },
        ),
    ]
