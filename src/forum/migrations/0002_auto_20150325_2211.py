# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import extra.utilities


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumfile',
            name='file',
            field=models.FileField(upload_to=extra.utilities.upload_file_to_function),
            preserve_default=True,
        ),
    ]
