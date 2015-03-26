# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tpo', '0006_auto_20150326_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ctc',
            field=models.DecimalField(max_digits=5, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
