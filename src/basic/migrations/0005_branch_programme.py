# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0004_userprofile_tpo'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='programme',
            field=models.CharField(default='B.Tech', max_length=10),
            preserve_default=False,
        ),
    ]
