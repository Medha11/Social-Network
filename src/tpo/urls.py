from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
	url(r'^$', views.home , name='tpo'),
	url(r'^add-company/$', views.add_company , name='add_company'),
	url(r'^company/$', views.company , name='company'),
	url(r'^company/(?P<company_id>\w+)/$', views.company , name='company'),
	url(r'^profile/$', views.profile , name='profile'),
	url(r'^profile/(?P<profile_id>\w+)/$', views.profile , name='profile'),
	url(r'^add-profile/$', views.add_profile , name='add_profile'),
	)