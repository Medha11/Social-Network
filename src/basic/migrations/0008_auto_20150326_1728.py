# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0007_auto_20150326_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='object_id',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
