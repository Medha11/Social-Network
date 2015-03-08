# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumanswer',
            name='file',
            field=models.FileField(upload_to=b'profile', blank=True),
            preserve_default=True,
        ),
    ]
