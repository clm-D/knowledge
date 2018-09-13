# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-12 01:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_name', models.CharField(max_length=10, unique=True, verbose_name='姓名')),
                ('s_age', models.IntegerField(default=16, verbose_name='年龄')),
                ('s_sex', models.BooleanField(default=1, verbose_name='性别')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('operate_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('math', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('chinese', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
            ],
            options={
                'db_table': 'student',
            },
        ),
    ]