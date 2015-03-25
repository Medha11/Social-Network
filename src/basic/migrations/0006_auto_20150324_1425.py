# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0005_branch_programme'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.CharField(max_length=20)),
                ('branch', models.ForeignKey(to='basic.Branch')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='course',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='branch',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='batch',
            field=models.ForeignKey(to='basic.Batch', null=True),
            preserve_default=True,
        ),
    ]
