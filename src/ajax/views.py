from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

import json
from forum.models import *
from extra.utilities import *

def follow(request):
	if request.method == 'GET':
		id = request.GET['question_id']
		if ForumQuestion.objects.filter(id=id).exists():
			student = getProfile(request)
			question = ForumQuestion.objects.get(id=id)
			if student in question.followers.all():
				success={'title':'Follow', 'text': '+'}
				Follows_Question.objects.get(question=question,student=student).delete()
				return HttpResponse(json.dumps(success),content_type="application/json")
			else:
				success={'title':'Unfollow', 'text': '-'}
				Follows_Question(question=question,student=student).save()
				return HttpResponse(json.dumps(success),content_type="application/json")
	
	return HttpResponseRedirect('/forum/'+course_id)