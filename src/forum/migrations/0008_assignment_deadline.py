# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_auto_20150306_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 7, 5, 23, 58, 979105, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
