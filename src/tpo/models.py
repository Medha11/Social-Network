from django.db import models

from extra.utilities import *

# Create your models here.
class Company(models.Model):
	name = models.CharField(max_length=100,unique=True)
	website = models.URLField(max_length=100, blank=True)
	logo = models.ImageField(upload_to='company_logos', blank=True)
	summary = models.TextField(blank=True)

	def __unicode__(self):
		return self.name

class Profile(models.Model):
	company = models.ForeignKey('Company')
	batches = models.ManyToManyField('basic.Batch', through='CompanyBatchMembership', 
						through_fields=('company', 'batch'))

	ctc = models.IntegerField(blank=True,null=True)

	def __unicode__(self):
		return str(self.company)

class CompanyBatchMembership(models.Model):
	company = models.ForeignKey('Profile')
	batch = models.ForeignKey('basic.Batch')
	def __unicode__(self):
		return str(self.branch)+'->'+str(self.company)
