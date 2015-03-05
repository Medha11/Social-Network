from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


from .models import *
from extra.utilities import *

# View for viewing forum and answers page
@login_required
def forum(request, course_id, question_id=None):

	user=getProfile(request)
	if authorize(user,course_id): #Checking if course exists and user is part of it
		if question_id: #Checking if display answer page
			if ForumQuestion.objects.filter(id=question_id).exists():  #Checking if question exists
				question = ForumQuestion.objects.get(id=question_id)
				answers = ForumAnswer.objects.filter(question = question)
				new_answers = []
				for answer in answers:
					new_answers.append(Answer(answer))
			return render(request,'forum/answers.html',{'question':question, 'answers':new_answers, 
						'User':user, 'course_id':course_id})

		else:
			course = Course.objects.get(id=course_id)
			 #Checking if user is enrolled
			questions = ForumQuestion.objects.filter(course = course)
			
			return render(request,'forum/forum.html',{'questions':questions,'User':user,'id':course_id})

		

		
	return HttpResponseRedirect('/')




@login_required
def delete_post(request,type="",course_id=None,post_id=None):
	user = getProfile(request)
	question_id = 0
	if authorize(user, course_id):
		if type == 'q':
			if ForumQuestion.objects.filter(id=post_id).exists(): #Checking if question exists
				question=ForumQuestion.objects.get(id=post_id)
				if user == question.user:
					question.delete()
				return HttpResponseRedirect('/forum/'+course_id)
		elif type =='a':
			if ForumAnswer.objects.filter(id=post_id).exists():
				answer=ForumAnswer.objects.get(id=post_id)
				if user == answer.user:
					answer.question.number_of_answers-=1
					answer.question.save()
					question_id = answer.question.id;
					answer.delete()
				return HttpResponseRedirect('/forum/'+course_id+'/'+str(question_id))
		else:
			if Comment.objects.filter(id=post_id).exists():
				comment=Comment.objects.get(id=post_id)
				if user == comment.user:
					comment.answer.number_of_comments-=1
					comment.answer.save()
					question_id = comment.answer.question.id;
					comment.delete()
				return HttpResponseRedirect('/forum/'+course_id+'/'+str(question_id))

	return HttpResponseRedirect('/')


# View for posting questions, answers and comments
@login_required
def post(request,course_id=None,question_id=None):
	user = getProfile(request)
	if authorize(user, course_id):
		if request.method=='POST':

			type = request.POST['type']
			anonymous = 'check' in request.POST.keys() #Checking if post should be anonymous
			if type=='question':
				title = request.POST['title']
				Question = request.POST['Question']
				Question=Question.replace('\n','<br>')
				ForumQuestion(title=title, question=Question, user=getProfile(request), 
					number_of_answers=0, course=Course.objects.get(id=course_id), 
					anonymous=anonymous).save()
				make_notification(course_id)
				return HttpResponseRedirect('/forum/'+course_id)
			elif type=='Answer':
				answer = request.POST['post'].replace('\n','<br>')
				if ForumQuestion.objects.filter(id=question_id).exists():
					cur_question = ForumQuestion.objects.get(id=question_id)
					cur_question.number_of_answers+=1
					cur_question.save()					
					ForumAnswer(answer=answer, user=user, question = cur_question, anonymous=anonymous).save()
					return HttpResponseRedirect('/forum/'+course_id+'/'+question_id)
			elif type=='Comment':
				comment = request.POST['post'].replace('\n','<br>')
				ans_id = request.POST['answer']
				if ForumAnswer.objects.filter(id=ans_id).exists():
					cur_answer = ForumAnswer.objects.get(id=ans_id)
					cur_answer.number_of_comments+=1
					cur_answer.save()
					Comment(comment=comment, user=user, answer = cur_answer, anonymous=anonymous).save()
					return HttpResponseRedirect('/forum/'+course_id+'/'+question_id)

		

	return HttpResponseRedirect('/')

