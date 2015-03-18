from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import *
from extra.utilities import *

# View for viewing forum and answers page
@login_required
def forum(request, course_id, question_id=None):

	user=getProfile(request)
	if authorize(user,course_id): # Checking if course exists and user is part of it
		if question_id: # Checking if display answer page
			if ForumQuestion.objects.filter(id=question_id).exists():  #Checking if question exists
				notifications = update_notifications(user, course_id,question_id)
				question = ForumQuestion.objects.get(id=question_id)
				if check_validity(question,course_id):
					answers = ForumAnswer.objects.filter(question = question).order_by('-date')
					new_answers = []
					for answer in answers:
						new_answers.append(Answer(answer))
					return render(request,'forum/answers.html',{'question':question, 'answers':new_answers, 
							'User':user, 'course_id':course_id, 'Notifications':notifications})

		else:
			notifications = update_notifications(user, course_id)
			course = Course.objects.get(id=course_id)
			questions = ForumQuestion.objects.filter(course = course).order_by('-date')
			assignments = Assignment.objects.filter(course = course).order_by('-date')
			files = ForumFile.objects.filter(course = course).order_by('-date')
			return render(request,'forum/forum.html',{'questions':questions,'User':user,'id':course_id, 
														'assignments':assignments,'files':files,
														'Notifications':notifications})

		
	return HttpResponseRedirect('/')




@login_required
def delete_post(request,type="",course_id=None,post_id=None):
	user = getProfile(request)
	question_id = 0
	if authorize(user, course_id):
		if type == 'q':
			if ForumQuestion.objects.filter(id=post_id).exists(): #Checking if question exists
				question=ForumQuestion.objects.get(id=post_id)
				if check_validity(question,course_id):
					if user.role == 'Faculty' or user == question.user: #confirming that the post belongs to user
						question.delete()
					return HttpResponseRedirect('/forum/'+course_id)
		elif type =='a':
			if ForumAnswer.objects.filter(id=post_id).exists():
				answer=ForumAnswer.objects.get(id=post_id)
				if check_validity(answer.question,course_id):
					if user.role == 'Faculty' or user == answer.user:
						answer.question.number_of_answers-=1
						answer.question.save()
						question_id = answer.question.id;
						answer.delete()
					return HttpResponseRedirect('/forum/'+course_id+'/'+str(question_id))
		elif type == 'c':
			if Comment.objects.filter(id=post_id).exists():
				comment=Comment.objects.get(id=post_id)
				if check_validity(comment.answer.question,course_id):
					if user.role == 'Faculty' or user == comment.user:
						comment.answer.number_of_comments-=1
						comment.answer.save()
						question_id = comment.answer.question.id;
						comment.delete()
					return HttpResponseRedirect('/forum/'+course_id+'/'+str(question_id))
		elif type == 'f':
			if ForumFile.objects.filter(id=post_id).exists():
				file=ForumFile.objects.get(id=post_id)
				if check_validity(file,course_id):
					if user.role == 'Faculty' or user == file.user:
						file.file.delete()
						file.delete()
					return HttpResponseRedirect('/forum/'+course_id+'/#file_tab')

		elif type == 'as':
			if Assignment.objects.filter(id=post_id).exists():
				assignment=Assignment.objects.get(id=post_id)
				if check_validity(assignment,course_id):
					if user.role == 'Faculty' or user == assignment.user:
						assignment.file.delete()
						assignment.delete()
					return HttpResponseRedirect('/forum/'+course_id+'/#assignment_tab')

	return HttpResponseRedirect('/')


# View for posting questions, answers and comments
@login_required
def post(request,course_id=None,object_id=None):
	user = getProfile(request)

	if authorize(user, course_id):
		if request.method=='POST':

			type = request.POST['type']
			anonymous = 'check' in request.POST.keys() #Checking if post should be anonymous
			if type=='question':
				title = request.POST['title']
				Question = request.POST['Question']
				Question=Question.replace('\n','<br>')
				question=ForumQuestion(title=title, question=Question, user=user, 
					number_of_answers=0, course=Course.objects.get(id=course_id), 
					anonymous=anonymous)
				question.save()
				make_notification(course_id,user,anonymous=anonymous)
				Follows_Question(question=question,student=user).save()
				return HttpResponseRedirect('/forum/'+course_id)
			elif type=='Answer':
				answer = request.POST['post'].replace('\n','<br>')
				if ForumQuestion.objects.filter(id=object_id).exists():
					cur_question = ForumQuestion.objects.get(id=object_id)
					if check_validity(cur_question,course_id):	
						cur_question.number_of_answers+=1
						cur_question.save()			
						ForumAnswer(answer=answer, user=user, question = cur_question, 
										anonymous=anonymous).save()
						make_notification(course_id,user, cur_question,anonymous=anonymous)
						return HttpResponseRedirect('/forum/'+course_id+'/'+object_id)

			elif type=='Comment':
				comment = request.POST['post'].replace('\n','<br>')
				ans_id = request.POST['answer']
				if ForumAnswer.objects.filter(id=ans_id).exists():
					cur_answer = ForumAnswer.objects.get(id=ans_id)
					if check_validity(cur_answer.question,course_id):
						cur_answer.number_of_comments+=1
						cur_answer.save()
						Comment(comment=comment, user=user, answer = cur_answer, anonymous=anonymous).save()
						return HttpResponseRedirect('/forum/'+course_id+'/'+object_id)

			elif type=='Assignment' and user.role == 'Faculty':
				title = request.POST['title']
				description = request.POST['description'].replace('\n','<br>')
				deadline = request.POST['date']
				course=Course.objects.get(id=course_id)
				date = deadline[6:]+'-'+deadline[:2]+'-'+deadline[3:5]
				if not description:
					description = 'No Description'
				new_assignment = Assignment(title=title, description=description, 
					course=course, deadline=date)
				
				if 'files' in request.FILES:
					create_zip(request.FILES.getlist('files'),user.id,new_assignment)
				else:
					new_assignment.save()
				for student in course.students.all():
					Pending(assignment=new_assignment,student=student).save()

				return HttpResponseRedirect('/forum/'+course_id+'/#assignment_tab')

			elif type=='File':
				title = request.POST['title']
				description = request.POST['description'].replace('\n','<br>')
				if not description:
					description = 'No Description'
				new_upload = ForumFile(title=title, description=description, 
					course=Course.objects.get(id=course_id),user = user)
				
				if 'files' in request.FILES:
					create_zip(request.FILES.getlist('files'),user.id,new_upload)
				else:
					new_upload.save()

				return HttpResponseRedirect('/forum/'+course_id+'/#file_tab')

			elif type=='Solution':
				if Assignment.objects.filter(id=object_id).exists():
					assignment = Assignment.objects.get(id=object_id)
					course=Course.objects.get(id=course_id)
					if check_validity(assignment,course_id):
						new_solution = AssignmentSolution(assignment= assignment, 
								course=course, user = user)
						new_solution.file = request.FILES['file']
						new_solution.save()
						Pending.objects.get(assignment=assignment,student=user).delete()
						return HttpResponseRedirect('/forum/'+course_id+'/#assignment_tab')

			elif type=='SolutionResubmit':
					assignment = Assignment.objects.get(id=object_id)
					if check_validity(assignment,course_id):
						try:
							print "dsa"
							solution = AssignmentSolution.objects.get(assignment= assignment,user = user)
							solution.file.delete()
							print "dsa"
							solution.file = request.FILES['file']
							solution.save()
							return HttpResponseRedirect('/forum/'+course_id+'/#assignment_tab')
						except:None

					

		

	return HttpResponseRedirect('/')



