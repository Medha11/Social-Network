from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import *
from extra.utilities import *
from extra.notifications import *




# Home page for tpo
@login_required
def home(request):

	user=getProfile(request)
	notifications = get_notifications(user)
	if user.tpo:
		profiles = Profile.objects.all().order_by('company__name')
		batches = create_batches()
		MixedProfiles = get_consolidated_profiles(profiles)
		return render(request,'tpo/tpo_home.html',{'MixedProfiles':MixedProfiles,'User':user,'batches':batches,
										'Notifications':notifications})
	else:
		eligiblities = Eligibility.objects.filter(student=user)
		profiles = []
		for eligiblity in eligiblities:
			profiles.append(eligiblity.company)
		return render(request,'tpo/home.html',{'User':user, 'profiles':profiles,
										'Notifications':notifications})
		
	return HttpResponseRedirect('/')


@login_required
def add_company(request):
	user=getProfile(request)
	if user.tpo:
		notifications = get_notifications(user)
		if request.method == 'POST':
			try:
				summary = request.POST['summary'].replace('\n','<br>')
				name = request.POST['name']
				website = request.POST['website']
				new_company = Company(name=name, website=website, summary=summary)
				if 'image' in request.FILES:
					new_company.logo = request.FILES['image']
				new_company.save()
				return HttpResponseRedirect('/tpo/')
			except: None
		return render(request,'tpo/add_company.html',{'User':user,'Notifications':notifications})
	return HttpResponseRedirect('/')

@login_required
def add_profile(request):
	user=getProfile(request)
	if user.tpo:
		notifications = get_notifications(user)
		if request.method == 'POST':
			type = request.POST['type']
			if type == 'selection':
				checklist = request.POST.getlist('check')
				companies = Company.objects.all().order_by('name')
				type = request.POST['profile_type']
				batches = Batch.objects.all()
				final_batches = []
				for item in checklist:
					programme,year = item.split(',')
					prog_batches = batches.filter(branch__programme=programme,year=year).order_by('branch__name')
					if prog_batches:
						final_batches.append(BatchClass(programme,prog_batches,year))
				return render(request,'tpo/add_profile.html',{'Batches':final_batches,'User':user,'type':type,
													'companies':companies,'Notifications':notifications})
			elif type == 'final':
				checklist = request.POST.getlist('check')
				company_id = int(request.POST['company'])
				ctc = request.POST['ctc']
				type = request.POST['profile_type']
				title = request.POST['profile']
				description = request.POST['description'].replace('\n','<br>')
				cpi = request.POST['cpi']
				if Company.objects.filter(id=company_id).exists():
					company = Company.objects.get(id=company_id)
					new_profile=Profile(company=company,cpi_cutoff=cpi,description=description,type=type,
															title=title,status='Registration')
					if ctc:
						new_profile.ctc=ctc
					new_profile.save()
					batches = []
					for item in checklist:
						batch = Batch.objects.get(id=int(item))
						batches.append(batch)
						CompanyBatchMembership(company=new_profile,batch=batch).save()
					make_tpo_notifications(new_profile,batches)
					

	return HttpResponseRedirect('/tpo/')

@login_required
def company(request,company_id):

	if Company.objects.filter(id=company_id).exists():
		user=getProfile(request)
		notifications = get_notifications(user)
		company = Company.objects.get(id=company_id)
		return render(request,'tpo/company.html',{'User':user,'company':company,'Notifications':notifications})
	return HttpResponseRedirect('/tpo/')

@login_required
def profile(request,profile_id):

	if Profile.objects.filter(id=profile_id).exists():
		user=getProfile(request)
		notifications = get_notifications(user)
		profile = Profile.objects.get(id=profile_id)
		new_Profile = get_consolidated_profile(profile,user)
		return render(request,'tpo/profile.html',{'User':user,'Profile':new_Profile,'Notifications':notifications})
	return HttpResponseRedirect('/tpo/')

@login_required
def delete(request,profile_id):
	user=getProfile(request)
	if Profile.objects.filter(id=profile_id).exists():
		profile = Profile.objects.get(id=profile_id)
		if Eligibility.objects.filter(student=user,company=profile).exists():
			Eligibility.objects.get(student=user,company=profile).delete()
			SetNotification.objects.get(user=user,keyword='tpo'+str(profile_id)).delete()
	return HttpResponseRedirect('/tpo/')

@login_required
def qualify(request,profile_id,user_name=None):
	user=getProfile(request)
	if Profile.objects.filter(id=profile_id).exists():
		profile = Profile.objects.get(id=profile_id)
		# if user_name and user.tpo: #for future qualifications 
		# 	requested_user = getProfile(request,username=user_name)
		# 	profile = Profile.objects.get(id=profile_id)
		# 	if Eligibility.objects.filter(student=requested_user,company=profile).exists():
		# 		Eligibility.objects.get(student=requested_user,company=profile).delete()
		# 		SetNotification.objects.get(user=requested_user,keyword='tpo'+str(profile_id)).delete()
		# 		Qualified(student=requested_user,company=profile).save()
		if profile.status == 'Registration':
			if Eligibility.objects.filter(student=user,company=profile).exists():
				SetNotification.objects.get(user=user,keyword='tpo'+str(profile_id)).delete()
				Qualified(student=user,company=profile).save()
	return HttpResponseRedirect('/tpo/')


@login_required
def candidates(request,profile_id):

	if Profile.objects.filter(id=profile_id).exists():
		user=getProfile(request)
		notifications = get_notifications(user)
		profile = Profile.objects.get(id=profile_id)
		candidates = profile.candidates.all().order_by('user__first_name','user__last_name')
		CandidateProfile = NewProfile(profile,candidates)
		return render(request,'tpo/candidates.html',{'User':user,'Profile':CandidateProfile,
											'Notifications':notifications})
	return HttpResponseRedirect('/tpo/')