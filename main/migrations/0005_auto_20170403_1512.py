# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-03 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20170401_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='file_record',
            name='link',
            field=models.URLField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='file_record',
            name='path',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
