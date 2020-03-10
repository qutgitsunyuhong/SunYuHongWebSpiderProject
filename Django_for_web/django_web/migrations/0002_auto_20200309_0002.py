# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2020-03-08 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='bookList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=30)),
                ('book_author', models.CharField(max_length=200)),
                ('book_publisher', models.CharField(max_length=30, null=True)),
                ('book_translator', models.CharField(max_length=30)),
                ('book_page_num', models.CharField(max_length=30, null=True)),
                ('book_score', models.FloatField(null=True)),
                ('book_rating_num', models.FloatField(null=True)),
                ('book_comm1', models.CharField(max_length=500)),
                ('book_comm2', models.CharField(max_length=500)),
                ('book_comm3', models.CharField(max_length=500)),
                ('book_comm4', models.CharField(max_length=500)),
                ('book_comm5', models.CharField(max_length=500)),
                ('book_stars1', models.FloatField(null=True)),
                ('book_stars2', models.FloatField(null=True)),
                ('book_stars3', models.FloatField(null=True)),
                ('book_stars4', models.FloatField(null=True)),
                ('book_stars5', models.FloatField(null=True)),
                ('kind', models.IntegerField(null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
