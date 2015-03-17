from django.db import models
from django.contrib.auth.models import User
from basic.models import *

# Create your models here.
class RssStore(models.Model):
	# This line is required. Links UserProfile to a User model instance.
	#user = models.OneToOneField(User)
	Title = models.CharField(max_length=200)
	Link = models.URLField( unique=True)
	Content = models.CharField(max_length = 500)
	#Category = models.ForeignKey(All_Interests,default=None)
	Category = models.CharField(max_length=40)


	#picture = models.ImageField(upload_to='profile_images', blank=True)

	def __unicode__(self):
		return self.Title