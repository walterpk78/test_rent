# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 21:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentomatic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transport',
            name='rented_until',
            field=models.DateTimeField(null=True),
        ),
    ]