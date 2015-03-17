# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllInterest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('course_id', models.CharField(unique=True, max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interest', models.ForeignKey(to='basic.AllInterest')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(to='basic.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100)),
                ('object_id', models.IntegerField(blank=True)),
                ('user_name', models.CharField(max_length=50)),
                ('link', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=32)),
                ('email', models.EmailField(unique=True, max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SetNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.CharField(max_length=100)),
                ('notification', models.ForeignKey(to='basic.Notification')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reg', models.CharField(unique=True, max_length=12)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('role', models.CharField(default=b'Student', max_length=20)),
                ('courses', models.ManyToManyField(to='basic.Course', through='basic.Membership')),
                ('notifications', models.ManyToManyField(to='basic.Notification', through='basic.SetNotification')),
                ('questions_followed', models.ManyToManyField(to='forum.ForumQuestion', through='forum.Follows_Question')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('user_interests', models.ManyToManyField(to='basic.AllInterest', through='basic.Interest')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='setnotification',
            name='user',
            field=models.ForeignKey(to='basic.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membership',
            name='student',
            field=models.ForeignKey(to='basic.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='interest',
            name='student',
            field=models.ForeignKey(to='basic.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to='basic.UserProfile', through='basic.Membership'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='allinterest',
            name='students',
            field=models.ManyToManyField(to='basic.UserProfile', through='basic.Interest'),
            preserve_default=True,
        ),
    ]
