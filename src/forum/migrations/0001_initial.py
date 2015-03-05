# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_register'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('anonymous', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.TextField()),
                ('number_of_comments', models.PositiveSmallIntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('anonymous', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=None, max_length=100)),
                ('question', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('number_of_answers', models.PositiveSmallIntegerField(default=0)),
                ('anonymous', models.BooleanField(default=False)),
                ('course', models.ForeignKey(default=None, to='basic.Course')),
                ('user', models.ForeignKey(to='basic.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='forumanswer',
            name='question',
            field=models.ForeignKey(to='forum.ForumQuestion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forumanswer',
            name='user',
            field=models.ForeignKey(to='basic.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='answer',
            field=models.ForeignKey(to='forum.ForumAnswer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to='basic.UserProfile'),
            preserve_default=True,
        ),
    ]
