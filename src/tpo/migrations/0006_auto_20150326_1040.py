# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tpo', '0005_auto_20150326_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='title',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
