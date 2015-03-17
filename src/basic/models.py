from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
	user = models.OneToOneField(User)
	reg = models.CharField(max_length=12, unique=True)
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	courses = models.ManyToManyField('Course', through='Membership', through_fields=('student', 'course'))
	notifications = models.ManyToManyField('Notification', through='SetNotification', 
						through_fields=('user', 'notification'))
	role = models.CharField(max_length=20, default="Student")
	user_interests = models.ManyToManyField('All_Interests',through='Interests', through_fields = ('student','interest'))

	questions_followed =  models.ManyToManyField('forum.ForumQuestion', through='forum.Follows_Question',
								 through_fields=('student', 'question'))

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
	students = models.ManyToManyField(UserProfile, through='Membership', through_fields=('course', 'student'))
	def __unicode__(self):
		return self.name

class Membership(models.Model):
	course = models.ForeignKey(Course)
	student = models.ForeignKey(UserProfile)


class All_Interests(models.Model):
	category = models.CharField(max_length=40)
	students = models.ManyToManyField(UserProfile, through='Interests', through_fields=('interest', 'student'))
	def __unicode__(self):
		return self.category


class Interests(models.Model):
	interest = models.ForeignKey(All_Interests)
	student = models.ForeignKey(UserProfile)



class Notification(models.Model):
	type = models.CharField(max_length=100)

# generic object for type
	object_id = models.IntegerField(blank = True)
	
	user_name = models.CharField(max_length=50)
	link = models.CharField(max_length=100)

	def __unicode__(self):
		return self.type



class SetNotification(models.Model):
	notification = models.ForeignKey(Notification)
	user = models.ForeignKey(UserProfile)
	link = models.CharField(max_length=100)