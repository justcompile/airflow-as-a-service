# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-15 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cluster',
            name='ui_endpoint',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]