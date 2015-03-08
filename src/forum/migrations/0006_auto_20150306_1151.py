# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_remove_assignment_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='assignment',
            field=models.FileField(upload_to=b'ass', blank=True),
            preserve_default=True,
        ),
    ]
