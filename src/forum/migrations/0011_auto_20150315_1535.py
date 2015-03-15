# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0009_setnotification_link'),
        ('forum', '0010_auto_20150311_0622'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follows_Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.ForeignKey(to='forum.ForumQuestion')),
                ('student', models.ForeignKey(to='basic.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='forumquestion',
            name='followers',
            field=models.ManyToManyField(to='basic.UserProfile', through='forum.Follows_Question'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forumquestion',
            name='user',
            field=models.ForeignKey(related_name='author', to='basic.UserProfile'),
            preserve_default=True,
        ),
    ]
