# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0006_auto_20150312_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='content_type',
        ),
        migrations.AlterField(
            model_name='notification',
            name='object_id',
            field=models.IntegerField(blank=True),
            preserve_default=True,
        ),
    ]
