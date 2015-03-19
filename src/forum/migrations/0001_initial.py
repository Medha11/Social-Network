# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import extra.utilities


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=None, max_length=100)),
                ('description', models.TextField(default=b'No Description')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField()),
                ('file', models.FileField(upload_to=extra.utilities.upload_to_function)),
                ('course', models.ForeignKey(to='basic.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AssignmentSolution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=extra.utilities.upload_solution_to_function)),
                ('date', models.DateTimeField(auto_now=True)),
                ('assignment', models.ForeignKey(to='forum.Assignment')),
                ('course', models.ForeignKey(to='basic.Course')),
                ('user', models.ForeignKey(to='basic.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
            name='Follows_Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
            name='ForumFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=None, max_length=100)),
                ('description', models.TextField(default=b'No Description', blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to=extra.utilities.upload_to_function)),
                ('course', models.ForeignKey(default=None, to='basic.Course')),
                ('user', models.ForeignKey(related_name='uploader', to='basic.UserProfile')),
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
                ('followers', models.ManyToManyField(to='basic.UserProfile', through='forum.Follows_Question')),
                ('user', models.ForeignKey(related_name='author', to='basic.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pending',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assignment', models.ForeignKey(to='forum.Assignment')),
                ('student', models.ForeignKey(to='basic.UserProfile')),
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
            model_name='follows_question',
            name='question',
            field=models.ForeignKey(to='forum.ForumQuestion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='follows_question',
            name='student',
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
