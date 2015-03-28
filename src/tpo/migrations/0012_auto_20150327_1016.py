# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0008_auto_20150326_1728'),
        ('tpo', '0011_profile_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Qualified',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.ForeignKey(to='tpo.Profile')),
                ('student', models.ForeignKey(to='basic.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='profile',
            name='candidates',
            field=models.ManyToManyField(to='basic.UserProfile', through='tpo.Qualified'),
            preserve_default=True,
        ),
    ]
