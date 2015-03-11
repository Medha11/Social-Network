# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import extra.utilities


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_auto_20150310_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentfile',
            name='assignment',
        ),
        migrations.DeleteModel(
            name='AssignmentFile',
        ),
        migrations.AddField(
            model_name='assignment',
            name='file',
            field=models.FileField(default=None, upload_to=extra.utilities.upload_to_function),
            preserve_default=False,
        ),
    ]
