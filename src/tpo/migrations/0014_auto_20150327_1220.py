# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tpo', '0013_auto_20150327_1219'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='qualified',
            options={'ordering': ('student__reg',)},
        ),
    ]
