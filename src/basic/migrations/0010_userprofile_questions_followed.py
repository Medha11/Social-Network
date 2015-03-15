# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_auto_20150315_1535'),
        ('basic', '0009_setnotification_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='questions_followed',
            field=models.ManyToManyField(to='forum.ForumQuestion', through='forum.Follows_Question'),
            preserve_default=True,
        ),
    ]
