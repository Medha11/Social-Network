# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import extra.utilities


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_assignment_deadline'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=extra.utilities.upload_to_function, blank=True)),
                ('assignment', models.ForeignKey(to='forum.Assignment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='assignment',
        ),
    ]
