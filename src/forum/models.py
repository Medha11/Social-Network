from django.db import models

from extra.utilities import *

# Create your models here.
class ForumQuestion(models.Model):
	title = models.CharField(max_length=100, default=None)
	question=models.TextField()
	user = models.ForeignKey('basic.UserProfile',related_name='author')
	date = models.DateTimeField(auto_now_add=True)
	number_of_answers = models.PositiveSmallIntegerField(default=0)
	course = models.ForeignKey('basic.Course', default=None)
	anonymous = models.BooleanField(default=False)
	followers =  models.ManyToManyField('basic.UserProfile', through='Follows_Question',
								 through_fields=('question', 'student'))

	def __unicode__(self):
		return self.title

class ForumAnswer(models.Model):
	answer=models.TextField()
	question = models.ForeignKey(ForumQuestion)
	number_of_comments = models.PositiveSmallIntegerField(default=0)
	user = models.ForeignKey('basic.UserProfile')
	date = models.DateTimeField(auto_now_add=True)
	anonymous = models.BooleanField(default=False)

	def __unicode__(self):
		return self.answer

class Comment(models.Model):
	comment = models.TextField()
	answer= models.ForeignKey(ForumAnswer)
	user = models.ForeignKey('basic.UserProfile')
	date = models.DateTimeField(auto_now_add=True)
	anonymous = models.BooleanField(default=False)

	def __unicode__(self):
		return self.comment

class Assignment(models.Model):
	title = models.CharField(max_length=100, default=None)
	description = models.TextField(default='No Description')
	date = models.DateTimeField(auto_now_add=True)
	course = models.ForeignKey('basic.Course')
	deadline = models.DateTimeField()
	file = models.FileField(upload_to=upload_to_function)

	def __unicode__(self):
		return self.title

class Pending(models.Model):
	student = models.ForeignKey('basic.UserProfile')
	assignment = models.ForeignKey('Assignment')

class AssignmentSolution(models.Model):
	assignment = models.ForeignKey('Assignment')
	file = models.FileField(upload_to=upload_solution_to_function)
	user = models.ForeignKey('basic.UserProfile')
	course = models.ForeignKey('basic.Course')
	date = models.DateTimeField(auto_now=True)

class Follows_Question(models.Model):
	question = models.ForeignKey(ForumQuestion)
	student = models.ForeignKey('basic.UserProfile')

class ForumFile(models.Model):
	title = models.CharField(max_length=100, default=None)
	description=models.TextField(blank=True,default='No Description')
	user = models.ForeignKey('basic.UserProfile',related_name='uploader')
	date = models.DateTimeField(auto_now_add=True)
	course = models.ForeignKey('basic.Course', default=None)
	file = models.FileField(upload_to=upload_to_function)

	def __unicode__(self):
		return self.title
	