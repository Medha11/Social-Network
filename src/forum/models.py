from django.db import models
from basic.models import *

# Create your models here.
class ForumQuestion(models.Model):
	title = models.CharField(max_length=100, default=None)
	question=models.TextField()
	user = models.ForeignKey(UserProfile)
	date = models.DateTimeField(auto_now_add=True)
	number_of_answers = models.PositiveSmallIntegerField(default=0)
	course = models.ForeignKey(Course, default=None)
	anonymous = models.BooleanField(default=False)

class ForumAnswer(models.Model):
	answer=models.TextField()
	question = models.ForeignKey(ForumQuestion)
	number_of_comments = models.PositiveSmallIntegerField(default=0)
	user = models.ForeignKey(UserProfile)
	date = models.DateTimeField(auto_now_add=True)
	anonymous = models.BooleanField(default=False)

class Comment(models.Model):
	comment = models.TextField()
	answer= models.ForeignKey(ForumAnswer)
	user = models.ForeignKey(UserProfile)
	date = models.DateTimeField(auto_now_add=True)
	anonymous = models.BooleanField(default=False)