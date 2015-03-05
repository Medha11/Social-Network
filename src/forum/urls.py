from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
	url(r'^$', views.forum , name='forum'),
	url(r'^(?P<course_id>\w+)/$', views.forum, name='forum_view'),
	url(r'^(?P<course_id>\w+)/(?P<question_id>\w+)/$', views.forum, name='forum_answer'),
	url(r'^post/$', views.post, name='post'),
	url(r'^post/delete/$', views.delete_post, name='delete_post'),
	url(r'^post/delete/(?P<type>\w+)/(?P<course_id>\w+)/(?P<post_id>\w+)/$', views.delete_post, name='delete_posts'),
	url(r'^post/(?P<course_id>\w+)/(?P<question_id>\w+)/$', views.post, name='posts'),
	)