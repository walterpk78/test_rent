# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-21 15:53
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('amount', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99900)])),
            ],
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transport_type', models.IntegerField(choices=[(b'bikes', 1), (b'cars', 2), (b'motorbikes', 3), (b'boats', 4)], db_index=True, null=True)),
                ('description', models.TextField(null=True)),
                ('price_per_day', models.BigIntegerField(default=0)),
                ('km', models.BigIntegerField(default=0, null=True)),
                ('rented', models.BooleanField(default=False)),
                ('rented_until', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='rent',
            name='transport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transport', to='rentomatic.Transport'),
        ),
    ]
