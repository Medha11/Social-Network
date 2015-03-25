from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import *
from extra.utilities import *




# Home page for tpo
@login_required
def home(request):

	user=getProfile(request)
	if user.tpo:
		profiles = Profile.objects.all()
		batches = create_batches()
		Profiles = get_consolidated_profiles(profiles)
		return render(request,'tpo/home.html',{'Profiles':Profiles,'User':user,'batches':batches})
		
	return HttpResponseRedirect('/')


@login_required
def add_company(request):
	user=getProfile(request)
	if user.tpo:
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
		return render(request,'tpo/add_company.html',{'User':user})
	return HttpResponseRedirect('/')

@login_required
def add_profile(request):
	user=getProfile(request)
	if user.tpo:
		if request.method == 'POST':
			type = request.POST['type']
			if type == 'selection':
				checklist = request.POST.getlist('check')
				companies = Company.objects.all().order_by('name')
				batches = Batch.objects.all()
				final_batches = []
				for item in checklist:
					programme,year = item.split(',')
					prog_batches = batches.filter(branch__programme=programme,year=year).order_by('branch__name')
					if prog_batches:
						final_batches.append(BatchClass(programme,prog_batches,year))
				return render(request,'tpo/add_profile.html',{'Batches':final_batches,'User':user,
													'companies':companies})
			elif type == 'final':
				checklist = request.POST.getlist('check')
				company_id = int(request.POST['company'])
				ctc = request.POST['ctc']
				if Company.objects.filter(id=company_id).exists():
					company = Company.objects.get(id=company_id)
					new_profile=Profile(company=company)
					if ctc:
						new_profile.ctc=ctc
					new_profile.save()
					for item in checklist:
						batch = Batch.objects.get(id=int(item))
						CompanyBatchMembership(company=new_profile,batch=batch).save()
					

	return HttpResponseRedirect('/tpo/')
