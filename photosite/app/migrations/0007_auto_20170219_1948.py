# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 19:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20170219_1947'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='group',
            new_name='company',
        ),
    ]
