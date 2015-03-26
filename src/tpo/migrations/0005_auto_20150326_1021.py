# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tpo', '0004_auto_20150325_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cpi_cutoff',
            field=models.DecimalField(default=None, max_digits=4, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='type',
            field=models.CharField(default=None, max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='ctc',
            field=models.DecimalField(default=None, max_digits=5, decimal_places=2),
            preserve_default=False,
        ),
    ]
