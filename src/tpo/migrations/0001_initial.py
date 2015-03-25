# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0006_auto_20150324_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(max_length=100, blank=True)),
                ('logo', models.ImageField(upload_to=b'company_logos', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyBatchMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('batch', models.ForeignKey(to='basic.Batch')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ctc', models.IntegerField(null=True, blank=True)),
                ('batches', models.ManyToManyField(to='basic.Batch', through='tpo.CompanyBatchMembership')),
                ('company', models.ForeignKey(to='tpo.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='companybatchmembership',
            name='company',
            field=models.ForeignKey(to='tpo.Profile'),
            preserve_default=True,
        ),
    ]
