# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0008_auto_20150313_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='setnotification',
            name='link',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
