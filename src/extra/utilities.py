from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from basic.models import *
from socnet import settings



############################################################################################
#####                                                                                 ######
#####                              UTILITY FUNCTIONS                                  ######
#####                                                                                 ######
#####                                                                                 ######
############################################################################################

def getProfile_user(request,username):
	if username == None:
		return UserProfile.objects.get(user=request.user)
	elif User.objects.filter(username=username).exists():
		return UserProfile.objects.get(user=User.objects.get(username=username))
	return None

def getProfile(request):
	if request.user.is_authenticated():
		return UserProfile.objects.get(user=request.user)
	return None

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

def authorize(profile, course_id):
	if profile.courses.all().filter(id=course_id).exists():
		return True
	return False

def make_notification(course_id):
	course = Course.objects.get(id=course_id)
	students = course.students.all()
	notification = 'A question has been posted in '+course.name
	link = '/forum/' + course_id
	new_notification=Notification(notification=notification, link=link)
	new_notification.save()
	for student in students:
		print student
		SetNotification(notification=new_notification,user=student).save()


#This class is used to create an object for the html which incorporates both answers and comments

class Answer():

	def __init__(self, answer):
		from forum.models import Comment
		self.answer = answer
		self.comments = Comment.objects.filter(answer=answer)

def upload_to_function(instance, filename): #function for dynamic file handling for assignments
	import os
	return os.path.join('assignment',instance.course.course_id,instance.title,filename)


def create_assignment(files,id,assignment):
	import os
	import zipfile	
	from django.core.files import File
	BASE = os.path.join(settings.BASE_DIR,'temp',id)
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
	assignment.file.save(assignment.title+'.zip',File(zipf))
	assignment.save()
	zipf.close()
	os.remove(ZIP)
	os.rmdir(BASE)

	
	

