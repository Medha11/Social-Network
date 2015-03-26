from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
	user = models.OneToOneField(User)
	batch = models.ForeignKey('Batch',null=True) 

	reg = models.CharField(max_length=12, unique=True, blank=True)
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	courses = models.ManyToManyField('Course', through='Membership', through_fields=('member', 'course'))
	notifications = models.ManyToManyField('Notification', through='SetNotification', 
						through_fields=('user', 'notification'))

	role = models.CharField(max_length=20, default="Student")
	tpo = models.BooleanField(default=False)

	cpi =  models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=2)
	user_interests = models.ManyToManyField('rss.Topic',through='rss.Interest', through_fields = ('student','topic'))

	questions_followed =  models.ManyToManyField('forum.ForumQuestion', through='forum.Follows_Question',
								 through_fields=('student', 'question'))

	pending_assignments = models.ManyToManyField('forum.Assignment', through='forum.Pending',
								 through_fields=('student', 'assignment'))

	def __unicode__(self):
		return self.user.username

class Register(models.Model):
	code = models.CharField(max_length=32, unique=True)
	email= models.EmailField(unique=True)
	def __unicode__(self):
		return self.email

class Course(models.Model):
	name = models.CharField(max_length=40)
	course_id = models.CharField(max_length=10, unique=True)
	students = models.ManyToManyField(UserProfile, through='Membership', through_fields=('course', 'member'))
	
	def __unicode__(self):
		return self.name

class Branch(models.Model):
	name = models.CharField(max_length=40)
	programme = models.CharField(max_length=10)
	def __unicode__(self):
		return self.name

class Batch(models.Model):
	year = models.CharField(max_length=20)
	branch = models.ForeignKey('Branch')
	def __unicode__(self):
		return self.year+'->'+str(self.branch)



class Membership(models.Model):
	course = models.ForeignKey(Course)
	member = models.ForeignKey(UserProfile)
	def __unicode__(self):
		return str(self.member)+'->'+str(self.course)



class Notification(models.Model):
	type = models.CharField(max_length=100)
	# generic object for type
	object_id = models.IntegerField()
	user_name = models.CharField(blank=True, max_length=50)
	link = models.CharField(max_length=100)

	def __unicode__(self):
		return self.type



class SetNotification(models.Model):
	notification = models.ForeignKey(Notification)
	user = models.ForeignKey(UserProfile)
	keyword = models.CharField(max_length=100)