# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import extra.utilities


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_register'),
        ('forum', '0002_forumanswer_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=None, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.FileField(upload_to=extra.utilities.upload_to_function, blank=True)),
                ('course', models.ForeignKey(default=None, to='basic.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='forumanswer',
            name='file',
        ),
    ]
