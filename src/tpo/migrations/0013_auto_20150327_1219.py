# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tpo', '0012_auto_20150327_1016'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eligibility',
            options={'ordering': ('student__reg',)},
        ),
    ]
