# Generated by Django 3.2.18 on 2023-03-26 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmts', '0002_auto_20230326_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='id',
            field=models.IntegerField(auto_created=True, max_length=20, primary_key=True, serialize=False, verbose_name='学院ID'),
        ),
    ]