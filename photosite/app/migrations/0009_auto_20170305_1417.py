# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-05 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_image_uploaditem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='data',
        ),
        migrations.AddField(
            model_name='image',
            name='full_size',
            field=models.ImageField(default='', upload_to='images/fullsize'),
        ),
        migrations.AddField(
            model_name='image',
            name='thumb',
            field=models.ImageField(default='', upload_to='images/thumbs'),
        ),
    ]
