from django.contrib.auth.models import User
from basic.models import *
from tpo.models import *
from extra.utilities import *

def update_notifications(user, id,question_id=None,assignment_id=None):  #functions deletes visited notifications
	link = '/forum/'+id
	if question_id:
		link+= '/'+question_id
	elif assignment_id:
		link=str(assignment_id)
	SetNotification.objects.filter(user=user,keyword=link).delete()
	return get_notifications(user)

def remove_notification(object_id,type,user_name=None,question_id=None): #remove notif on delete
	if not user_name:
		user_name=''
	if Notification.objects.filter(type=type, object_id=object_id,user_name=user_name).exists():
			Notification.objects.filter(type=type, object_id=object_id,user_name=user_name)[0].delete()
	if type == 'Question': #removing notifications of answers linked to question
		if Notification.objects.filter(type=type, object_id=question_id).exists():
			Notification.objects.filter(type=type, object_id=question_id).delete()


def make_tpo_notifications(profile,batches):
	id = str(profile.id)
	link = '/tpo/profile/' + id
	new_notification = Notification(type='TPO', link=link,object_id = profile.id)
	new_notification.save()
	for batch in batches:
		students = UserProfile.objects.filter(batch=batch,cpi__gte=profile.cpi_cutoff)
		for student in students:
			SetNotification(notification=new_notification,user=student,keyword='tpo'+id).save()
			Eligibility(student=student,company=profile).save()


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


	elif assignment_id: #creating notif for assignment
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


	
class ConsolidatedNotifications: #class for returning consolidated notifications

	def __init__(self, notification, link):
		self.notification = notification
		self.link = link 


def get_notifications(user): #function for consolidated notifications
	list = []
	for assignment in user.pending_assignments.all():
		check_assignment(assignment.id)
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

	if user.notifications.filter(type='TPO').exists():
		profiles = user.notifications.filter(type='TPO')
		for profile in profiles:
			object = Profile.objects.get(id=profile.object_id)
			notification = frame_tpo_notification(object)
			list.append(ConsolidatedNotifications(notification,profile.link))
			
	return list


def frame_tpo_notification(profile):
	if profile.type == 'Job':
		type = 'a <strong>job</strong>'
	else:
		type = 'an <strong>internship</strong>'
	notification = '<strong>'+profile.company.name+'</strong> has '+ type + ' that you are eligible for!!!'

	return notification

def frame_assignment_notification(length,course):
	if length > 1:
		notification = 'You have <strong>'+str(length)+' '+course.name+'</strong> assignments pending.'
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


