from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
	url(r'^$', views.home , name='tpo'),
	url(r'^company$', views.add_company , name='add_company'),
	url(r'^profile$', views.add_profile , name='add_profile'),
	)