# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rss', '0001_initial'),
        ('forum', '0001_initial'),
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='pending_assignments',
            field=models.ManyToManyField(to='forum.Assignment', through='forum.Pending'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='questions_followed',
            field=models.ManyToManyField(to='forum.ForumQuestion', through='forum.Follows_Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_interests',
            field=models.ManyToManyField(to='rss.Topic', through='rss.Interest'),
            preserve_default=True,
        ),
    ]
