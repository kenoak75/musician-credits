# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-25 00:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musiciancredits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recording',
            name='cover',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]