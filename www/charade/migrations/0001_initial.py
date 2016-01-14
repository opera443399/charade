# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-14 10:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameScoreBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, verbose_name='\u5355\u8bcd\u603b\u6570')),
                ('scores', models.IntegerField(default=0, verbose_name='\u603b\u5f97\u5206')),
                ('dt_start', models.DateTimeField(auto_now_add=True, verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('dt_end', models.DateTimeField(auto_now=True, verbose_name='\u7ed3\u675f\u65f6\u95f4')),
            ],
        ),
        migrations.CreateModel(
            name='GameTemporaryTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('en', models.CharField(max_length=200, verbose_name='en')),
                ('zh', models.CharField(max_length=100, verbose_name='\u4e2d\u6587')),
                ('exp', models.TextField(null=True, verbose_name='\u89e3\u91ca')),
                ('scores', models.IntegerField(default=0, verbose_name='\u5f97\u5206')),
                ('used', models.IntegerField(default=0, verbose_name='used')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charade.GameScoreBoard')),
            ],
        ),
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('en', models.CharField(max_length=200, unique=True, verbose_name='en')),
                ('zh', models.CharField(max_length=100, verbose_name='\u4e2d\u6587')),
                ('exp', models.TextField(null=True, verbose_name='\u89e3\u91ca')),
                ('dt', models.DateTimeField(auto_now_add=True, verbose_name='\u65f6\u95f4')),
            ],
        ),
    ]
