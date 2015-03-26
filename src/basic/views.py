from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import *
from rss.models import *
from extra.utilities import *
from extra.notifications import *
import uuid

def home(request):
	user=getProfile(request)
	if user:
		notifications = get_notifications(user)
		feeds = getRSS(user)
		return render(request, 'basic/user_homepage.html',{'User':user,'Notifications':notifications,'feeds':feeds})
	return render(request, 'basic/homepage.html',{'type':"First"}) #type registration type

def user_login(request):
	if request.method == 'POST' and not request.user.is_authenticated():
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, 	password=password)
		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence 	of a value), no user
		# with matching credentials was found.
		if user:
		# Is the account active? It could have been 	disabled.
			if user.is_active:
		# If the account is valid and active, we can 	log the user in.
		# We'll send the user back to the homepage.
				login(request, user)
				return HttpResponseRedirect('/')
			else:
		# An inactive account was used - no logging 	in!
				return HttpResponse("Your Account is disabled.")
		else:
		# Bad login details were provided. So we can't 		log the user in.
			print "Invalid login details: {0}, 	{1}".format(username, password) 
			return render(request,'basic/login.html',{'display':True})
		# The request is not a HTTP POST, so display the login 		form.
		# This scenario would most likely be a HTTP GET.
		

	else:
	# No context variables to pass to the template 	system, hence the
	# blank dictionary object...
		return HttpResponseRedirect('/')


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
# Since we know the user is logged in, we can now just log them out.
	logout(request)
# Take the user back to the homepage.
	return HttpResponseRedirect('/')


def register(request,code=None):

	context={}
	if request.method == 'POST':
		try: # handling bad POST packets
			context['label']=True		
			context['type']= 'danger'
			type = request.POST['type']
			if type=="First": #checking if initiating registration
				email = request.POST['email']
				if email.endswith('@mnnit.ac.in'):	
					if User.objects.filter(email=email).exists():
						context['message']='There is already an account with this Email Address!!!!'
						context['tag']='Sorry!'
						print "dasasd"
						return render(request, 'basic/homepage.html', context)

					unique_code=uuid.uuid4().hex
					if Register.objects.filter(email=email).exists():
						entry=Register.objects.get(email=email)
						unique_code=str(entry.code)
					else:
						#finding a unique_code
						while Register.objects.filter(code=unique_code).exists():
							unique_code=uuid.uuid4().hex
						new_entry=Register(email=email,code=unique_code)
						new_entry.save()
					
					if confirmation(email,unique_code): #sending email
						context['type']= 'success'
						context['message']='A confirmation mail will be sent shortly to the email address you provided!!!!'
						context['tag']='Great!'
					else: #mail not sent
						context['tag']='Sorry!'
						context['message']='The server is unable to process your request. Please try again later or contact the Administrator!!!!'
				
				else: #not mnnit email
					context['message']='Registration Failed!!!!'
					context['tag']='Error!'
					context['mnnit']=True
				return render(request, 'basic/homepage.html', context)

			else: # registration step 2
				email = request.POST['email']
				code = request.POST['code']
				fname = request.POST['fname']
				lname = request.POST['lname']
				reg = request.POST['reg']
				password = request.POST['password']
				username = request.POST['username']
				if not Register.objects.filter(email=email).exists():
					return HttpResponseRedirect('/')
				if Register.objects.get(email=email).code != code:
					context['message']='Nice Try!!!!'
					context['tag']='Hacker Alert!'
					return render(request,'basic/homepage.html', context)
				if User.objects.filter(username=username).exists():
					context['email']=email
					context['fname']=fname
					context['lname']=lname
					context['reg']=reg
					context['not_unique']=True
					return render(request,'basic/register.html', context)

				user=User.objects.create_user(email=email,first_name=fname, last_name=lname, 
					username=username, password=password)
				UserProfile(user=user,reg=str(reg)).save()
				context['type']= 'success'
				context['message']='Registration Successful. You can now login!!!!'
				context['tag']='Congratulations!'
				Register.objects.get(email=email).delete()
				if request.user.is_authenticated():
					logout(request)
				return render(request, 'basic/homepage.html', context)

		except: return HttpResponseRedirect('/') #bad POST

	# redirecting to step 2

	if not Register.objects.filter(code=code).exists(): #checking if valid code
		return HttpResponseRedirect('/')

	context['email']=Register.objects.get(code=code).email
	context['code']=code
	context['type'] = "Second"
	return render(request, 'basic/register.html',context) # redirecting to step 2


@login_required
def user_profile(request, username=None):
# Since we know the user is logged in, we can now just log them out.
# Take the user back to the homepage.
	user=getProfile(request,username)
	notifications = get_notifications(getProfile(request))
	if request.method == 'POST':
		try:
			type = request.POST['type']		
			if type == "edit":
				return render(request,'basic/profile.html',{'button':'Save',
					'UserReq':user, 'User':getProfile(request),'type':'save', 'Notifications':notifications})
			
			lname = request.POST['lname']
			email = request.POST['email']
			fname = request.POST['fname']
			if request.user.email == email:
				request.user.first_name = fname
				request.user.last_name = lname
				request.user.save()

		except: return HttpResponseRedirect('/')

	return render(request,'basic/profile.html',{'property':True, 'button':'Edit',
				 'UserReq':user, 'User':getProfile(request),'type':'edit', 'Notifications':notifications})

