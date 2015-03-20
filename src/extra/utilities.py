from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from basic.models import *

from socnet import settings
from rss.models import *


############################################################################################
#####                                                                                 ######
#####                              UTILITY FUNCTIONS                                  ######
#####                                                                                 ######
#####                                                                                 ######
############################################################################################

def getProfile(request,username=None):
	if username == None: #sending current user's profile
		if request.user.is_authenticated():
			return UserProfile.objects.get(user=request.user)
	elif User.objects.filter(username=username).exists():
		return UserProfile.objects.get(user=User.objects.get(username=username))
	return None

def getRSS(user):	
	feeds = []
	for topic in user.user_interests.all():
		feeds += RSSStore.objects.filter(Category=topic)
	return feeds	



############################################################################################
#####                                                                                 ######
#####                              Notifications                                      ######
#####                                                                                 ######
#####                                                                                 ######
############################################################################################

def remove_notification(object_id,type,user_name=None,question_id=None):	
	if not user_name:
		user_name=''
	if Notification.objects.filter(type=type, object_id=object_id,user_name=user_name).exists():
			Notification.objects.filter(type=type, object_id=object_id,user_name=user_name)[0].delete()
	if type == 'Question':
		if Notification.objects.filter(type=type, object_id=question_id).exists():
			Notification.objects.filter(type=type, object_id=question_id).delete()

def make_notification(course_id,user, question=None, anonymous=False,assignment_id=None): #TODO Reuse code !!!!!!!!!!
	course = Course.objects.get(id=course_id)
	if question: # creating notifications for answers

		students = question.followers.all()
		link = '/forum/' + course_id + '/' + str(question.id)
		object_id = question.id
		if anonymous:
			user_name = 'Anonymous'
		else:
			user_name = user.user.first_name
		new_notification=Notification(type='Answer',user_name = user_name, link=link, 
							object_id=object_id)
		new_notification.save()
		for student in students:
			SetNotification(notification=new_notification,user=student,keyword=link).save()


	elif assignment_id:
		students = course.students.all().filter(role='Student')
		link = '/forum/' + course_id + '/#assignment_tab'
		object_id = course.id
		new_notification=Notification(type='Assignment',link=link, object_id=object_id)
		new_notification.save()
		for student in students:
			SetNotification(notification=new_notification,user=student,keyword=str(assignment_id)).save()

	else: #notifications for questions
		students = course.students.all()
		link = '/forum/' + course_id
		object_id = course.id
		if anonymous:
			user_name = 'Anonymous'
		else:
			user_name = user.user.first_name
		new_notification=Notification(type='Question',user_name = user_name, link=link, object_id=object_id)
		new_notification.save()
		for student in students:
			SetNotification(notification=new_notification,user=student,keyword=link).save()


def get_notifications(user): #function for consolidated notifications
	list = []
	if user.notifications.filter(type='Question').exists():
		questions = user.notifications.filter(type='Question')
		for course in user.courses.all():
			course_questions = questions.filter(object_id=course.id)
			if course_questions:
				length = len(course_questions)
				names = course_questions.values("user_name").distinct()
				unique_length = len(names)
				notification = frame_question_notification(unique_length,length,names,course)
				if notification:
					list.append(ConsolidatedNotifications(notification,course_questions[0].link))

	if user.notifications.filter(type='Answer').exists():
		answers = user.notifications.filter(type='Answer')
		for question in user.questions_followed.all():
			question_answers = answers.filter(object_id=question.id)
			if question_answers:
				names = question_answers.values("user_name").distinct()
				title = question.title
				if len(title)>15:
					title = title[:14]+'...'
				title = '<span style="font-size:13px;font-style: italic;">"'+title+'"</span>'
				unique_length = len(names)
				notification = frame_answer_notification(unique_length,title,names,question.course)
				if notification:
					list.append(ConsolidatedNotifications(notification,question_answers[0].link))

	if user.notifications.filter(type='Assignment').exists():
		assignments = user.notifications.filter(type='Assignment')
		for course in user.courses.all():
			course_assignments = assignments.filter(object_id=course.id)
			if course_assignments:
				length = len(course_assignments)
				notification = frame_assignment_notification(length,course)
				if notification:
					list.append(ConsolidatedNotifications(notification,course_assignments[0].link))
			
	return list

def frame_assignment_notification(length,course):
	if length > 1:
		notification = 'You have <strong>'+course.name+'</strong> assignments pending.'
	else:
		notification = 'You have a <strong>'+course.name+'</strong> assignment pending.'

	return notification

def frame_question_notification(unique_length, length, names,course): #framing notifications
	notification = None
	if unique_length == 1:
		notification = '<strong>' + names[0]['user_name'] +'</strong>'
		if length == 1:
			notification += ' asked a question in the ' 
		else:
			notification += ' asked questions in the '
		notification+= '<strong>' + course.name + '</strong> forum'
	elif unique_length == 2:
		user1 = names[0]['user_name']
		user2 =	names[1]['user_name']
		
		notification = '<strong>'+user1+'</strong>' + ' and ' 
		notification+= '<strong>'+user2+'</strong>'
		notification+= ' asked questions in the ' + '<strong>'+course.name + '</strong> forum'

	elif unique_length > 2:
		user1 = names[0]['user_name']
		notification = '<strong>' + user1+'</strong>' + ' and <strong>' + str(unique_length-1) 
		notification+= ' others</strong>  asked questions in the ' + '<strong>'
		notification+= course.name + '</strong> forum'
	
	return notification

def frame_answer_notification(unique_length, question, names,course):
	notification = None
	if unique_length == 1:
		notification = '<strong>' + names[0]['user_name'] +'</strong> answered the question ' + question 
		notification+= ' in the <strong>' + course.name + '</strong> forum'
	elif unique_length == 2:
		user1 = names[0]['user_name']
		user2 =	names[1]['user_name']
		
		notification = '<strong>'+user1+'</strong>' + ' and ' 
		notification+= '<strong>'+user2+'</strong>'
		notification+= ' answered the question '+question+' in the ' + '<strong>'+course.name + '</strong> forum'

	elif unique_length > 2:
		user1 = names[0]['user_name']
		notification = '<strong>' + user1+'</strong>' + ' and <strong>' + str(unique_length-1) 
		notification+= ' others</strong>  answered the question'+question+' in the ' + '<strong>'
		notification+= course.name + '</strong> forum'
	
	return notification

	
class ConsolidatedNotifications: #class for returning consolidated notifications

	def __init__(self, notification, link):
		self.notification = notification
		self.link = link 

class AssignmentClass: #class for returning consolidated notifications
	
	def __init__(self, assignment, user):
		from forum.models import AssignmentSolution
		self.assignment = assignment
		if user.role == 'Student':
			if AssignmentSolution.objects.filter(user=user,assignment=assignment).exists():
				self.solution =  AssignmentSolution.objects.get(user=user,assignment=assignment)


def update_notifications(user, id,question_id=None,assignment_id=None):  #functions deletes visited notifications
	link = '/forum/'+id
	if question_id:
		link+= '/'+question_id
	elif assignment_id:
		link=str(assignment_id)
	SetNotification.objects.filter(user=user,keyword=link).delete()
	return get_notifications(user)


############################################################################################
#####                                                                                 ######
#####                              Confirmation mail                                  ######
#####                                                                                 ######
#####                                                                                 ######
############################################################################################

#confimation mail
def confirmation(email,unique_code):

	sub = 'Confirmation Email'
	message='Hello '+email+',\n \t This Email was automatically generated when you tried to register on The SocNet. '
	message+='So please do not reply to this Email.\n'
	message+='\n\n\t To continue with your registration please click on the link below. If the link does not appear, '
	message+='please copy the URL onto your browser\'s address bar.\n\n'
	message+='http://127.0.0.1:8000/register/'+unique_code 
	message+='\n\nThank you for registering with us.'
	message+='\nRegards,\nThe SocNet Team'
	from_email= settings.EMAIL_HOST_USER
	to = [email, from_email]
	for i in range(3):
		try:
			send_mail(subject=sub,message=message,from_email=from_email,recipient_list=to)
			return True
		except: None
	return False

############################################################################################
#####                                                                                 ######
#####                              Validity                                           ######
#####                                                                                 ######
#####                                                                                 ######
############################################################################################

def authorize(profile, course_id):
	if profile.courses.filter(id=course_id).exists():
		return True
	return False

def check_validity(object, course_id): #function checks if object belongs to course
		return str(object.course.id) == str(course_id)


#This class is used to create an object for the html which incorporates both answers and comments

class Answer:
	def __init__(self, answer):
		from forum.models import Comment
		self.answer = answer
		self.comments = Comment.objects.filter(answer=answer).order_by('-date')


############################################################################################
#####                                                                                 ######
#####                              FILE Handling                                      ######
#####                                                                                 ######
#####                                                                                 ######
############################################################################################

def upload_to_function(instance, filename): #function for dynamic file handling for assignments
	import os
	return os.path.join('files',instance.course.course_id,filename)

def upload_solution_to_function(instance, filename): #function for dynamic file handling for assignments
	import os
	return os.path.join('files',instance.course.course_id,'solutions',filename)


def create_zip(files,id,object): #stores in temp folder, zips, saves and removes the temp files
	import os
	import zipfile	
	from django.core.files import File
	BASE = os.path.join(settings.BASE_DIR,'temp',str(id))
	try:
		os.makedirs(BASE)
	except: None
	os.chdir(BASE)
	zipf = zipfile.ZipFile('Python.zip', 'w')
	for file in files:
		file_path = os.path.join(BASE,file.name)
		with open(file_path, 'wb+') as destination:
			for chunk in file.chunks():
				destination.write(chunk)
			destination.close()
		zipf.write(file.name)
		os.remove(file.name)
	zipf.close()
	ZIP = os.path.join(BASE,'Python.zip')
	zipf=open(ZIP)
	object.file.save(object.title+'.zip',File(zipf))
	object.save()
	zipf.close()
	os.remove(ZIP)
	os.rmdir(BASE)



	


