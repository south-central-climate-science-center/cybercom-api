from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.models import Permission
from api.views import APIRoot, UserProfile #, UserView
#from rest_framework import routers

try:
    admin.site.register(Permission)
except:
    pass

admin.autodiscover()

#router=routers.SimpleRouter()
#router.register(r'accounts', UserView, 'list')

urlpatterns = patterns('',
    #url(r'^api/', include(router.urls)),
    # Django Rest Login Urls
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Queue Application
    url(r'^queue/', include('queue.urls')),
    url(r'^data_store/',include('data_store.urls')),
    url(r'^catalog/', include('catalog.urls')),
    # Admin Urls
    url(r'^admin/', include(admin.site.urls)),
    # Main Project View - Customize depending on what Apps are enabled
    url(r'^$', APIRoot.as_view()),
    url(r'^/\.(?P<format>(api|json|jsonp|xml|yaml))/$', APIRoot.as_view()),
    # User Profile
    url(r'^user/',UserProfile.as_view(),name='user-list'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

)
