# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('basic', '0005_delete_taggeditem'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='content_type',
            field=models.ForeignKey(default=None, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='object_id',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
    ]
