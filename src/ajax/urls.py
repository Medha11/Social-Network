from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
	url(r'^$', views.follow , name='ajax'),
	
	url(r'^follow/$', views.follow, name='follow'),
	#url(r'^post/delete/(?P<type>\w+)/(?P<course_id>\w+)/(?P<post_id>\w+)/$', views.delete_post, name='deletase_posts'),	
	
	)