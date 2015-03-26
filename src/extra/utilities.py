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
#####                              Assignment                                         ######
#####                                                                                 ######
#####                                                                                 ######
############################################################################################


class AssignmentClass: #class for returning consolidated assignment with solution details
	
	def __init__(self, assignment, user):
		from forum.models import AssignmentSolution
		self.assignment = assignment
		if user.role == 'Student':
			if AssignmentSolution.objects.filter(user=user,assignment=assignment).exists():
				self.solution =  AssignmentSolution.objects.get(user=user,assignment=assignment)





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
	return os.path.join(instance.course.course_id,'assignments',filename)

def upload_solution_to_function(instance, filename): #function for dynamic file handling for assignment solutions
	import os
	return os.path.join(instance.course.course_id,'assignments','solutions',filename)

def upload_file_to_function(instance, filename): #function for dynamic file handling for file uploads
	import os
	return os.path.join(instance.course.course_id,'files',filename)


#used for assignment and files
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


############################################################################################
#####                                                                                 ######
#####                                 TPO                                             ######
#####                                                                                 ######
#####                                                                                 ######
############################################################################################


class BatchClass:

	def __init__(self, programme, batches,year):
		self.programme = programme
		self.batches = batches
		self.year=year

class BatchListClass:

	def __init__(self, programme, years):
		self.programme = programme
		self.years = years 
 
class ConsolidatedProfiles:

	def __init__(self, profile, batches):
		self.profile = profile
		self.batches = batches 

def create_batches(): #Creates a list of objects containing prog and years
	from basic.models import Batch
	batches = Batch.objects.all().order_by('branch__programme','year')
	list = batches.values('branch__programme','year').distinct()
	final = {}
	for item in list:
		programme = item['branch__programme']
		year = item['year']
		if final.get(programme):
			final[programme].append(year)
		else:
			final[programme]=[year]
	batches=[]
	keys = final.keys()
	keys.sort()
	for programme in keys:
		batches.append(BatchListClass(programme,final[programme]))
	return batches

def get_consolidated_profiles(profiles):
	Profiles = []
	for profile in profiles:
		batches = profile.batches.order_by('branch__programme','year')
		list = batches.values('branch__programme','year').distinct()
		final_batches=[]
		for item in list:
			programme = item['branch__programme']
			year = item['year']
			same_batch = batches.filter(branch__programme=programme, year=year).order_by('branch__name')
			if same_batch:
				final_batches.append(BatchClass(programme,same_batch,year))
		Profiles.append(ConsolidatedProfiles(profile,final_batches))
	return Profiles

def get_consolidated_profile(profile):

	batches = profile.batches.order_by('branch__programme','year')
	list = batches.values('branch__programme','year').distinct()
	final_batches=[]
	for item in list:
		programme = item['branch__programme']
		year = item['year']
		same_batch = batches.filter(branch__programme=programme, year=year).order_by('branch__name')
		if same_batch:
			final_batches.append(BatchClass(programme,same_batch,year))
	Profile=ConsolidatedProfiles(profile,final_batches)
	return Profile




