# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-21 04:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import impressGenerator.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_src', models.TextField()),
                ('page_order', models.SmallIntegerField()),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('z', models.IntegerField()),
                ('rx', models.SmallIntegerField()),
                ('ry', models.SmallIntegerField()),
                ('rz', models.SmallIntegerField()),
                ('scale', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('token', models.CharField(default=impressGenerator.models.random_token, max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='presentation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impressGenerator.Presentation'),
        ),
    ]
