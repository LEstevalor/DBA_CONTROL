# Generated by Django 3.2.18 on 2023-03-26 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0004_auto_20230326_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='college_id',
            field=models.IntegerField(verbose_name='学院ID'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='major_id',
            field=models.IntegerField(verbose_name='专业ID'),
        ),
        migrations.AlterField(
            model_name='teach_research_office',
            name='college_id',
            field=models.IntegerField(verbose_name='学院ID'),
        ),
    ]
