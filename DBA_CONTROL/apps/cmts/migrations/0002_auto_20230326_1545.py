# Generated by Django 3.2.18 on 2023-03-26 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='id',
            field=models.CharField(auto_created=True, max_length=20, primary_key=True, serialize=False, verbose_name='学院ID'),
        ),
        migrations.AlterField(
            model_name='major',
            name='id',
            field=models.CharField(auto_created=True, max_length=20, primary_key=True, serialize=False, verbose_name='专业ID'),
        ),
    ]
