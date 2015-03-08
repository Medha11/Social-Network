# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20150306_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='code',
            field=models.CharField(default='sadda', unique=True, max_length=32),
            preserve_default=False,
        ),
    ]
