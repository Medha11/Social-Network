# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import extra.utilities


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20150306_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='assignment',
            field=models.FileField(upload_to=extra.utilities.upload_to_function, blank=True),
            preserve_default=True,
        ),
    ]
