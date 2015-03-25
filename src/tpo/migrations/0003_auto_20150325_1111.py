# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tpo', '0002_company_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='summary',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
