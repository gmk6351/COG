# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-09 15:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cog', '0007_auto_20160303_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='type',
            field=models.CharField(choices=[(b'blog', b'Blog'), (b'page', b'Page'), (b'hyperlink', b'Hyperlink'), (b'notes', b'Notes')], max_length=10, verbose_name=b'Type'),
        ),
    ]
