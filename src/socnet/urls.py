from django.conf.urls import patterns, include, url
from django.contrib import admin
from basic import views
from . import settings 

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'socnet.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^register/$', views.register, name='register'),
	url(r'^register/(?P<code>\w+)/$', views.register, name='register_resume'),	
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^profile/$', views.user_profile, name='profile'),
	url(r'^profile/(?P<username>\w+)/$', views.user_profile, name='profiles'),
	url(r'^forum/', include('forum.urls'), name='forum'),
)

if settings.DEBUG:
	urlpatterns += patterns('django.views.static', (r'^media/(?P<path>.*)',
		'serve', {'document_root': settings.MEDIA_ROOT}), )
