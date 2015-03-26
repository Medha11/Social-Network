# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0006_auto_20150324_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cpi',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='object_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='user_name',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
