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
	title = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	company = models.ForeignKey('Company')
	batches = models.ManyToManyField('basic.Batch', through='CompanyBatchMembership', 
						through_fields=('company', 'batch'))
	type = models.CharField(max_length=12)
	ctc = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
	cpi_cutoff = models.DecimalField(max_digits=4, decimal_places=2)
	status = models.CharField(max_length=20)

	def __unicode__(self):
		return str(self.company)

class CompanyBatchMembership(models.Model):
	company = models.ForeignKey('Profile')
	batch = models.ForeignKey('basic.Batch')
	def __unicode__(self):
		return str(self.batch)+'->'+str(self.company)

class Eligibility(models.Model):
	company = models.ForeignKey('Profile')
	student = models.ForeignKey('basic.UserProfile')
	def __unicode__(self):
		return str(self.student)+'->'+str(self.company)