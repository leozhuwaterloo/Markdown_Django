# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-03 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waterlooworks', '0002_auto_20170202_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='organization_price',
            field=models.CharField(default='', max_length=50),
        ),
    ]