__author__ = 'mstacy'
from django.conf.urls import patterns, url
from django.contrib import admin
from cybercom_queue.views import Run, Queue, UserTasks, UserResult,flushMemcache
from rest_framework.urlpatterns import format_suffix_patterns

# q = QueueTask()
#tasks_url = []

#for task in q.list()['available_tasks']:
#    tasks_url.append(url(r'%s/$' % task, Run.as_view(), name="%s-run" % (task)))
#    #tasks_url.append(url(r'%s/.(api|json|jsonp|xml|yaml)$' % task, Run.as_view(), name="%s-run-format" % (task)))

admin.autodiscover()

urlpatterns = patterns('',
                       #url(r'run/', include(tasks_url)),
                       #url(r'run/$',Run.as_view(),name='run-main'),
                       url(r'run/(?P<task_name>[-\w .]+)/$', Run.as_view(), name='run-main'),
                       url(r'task/(?P<task_id>[-\w]+)/$', UserResult.as_view(), name='queue-task-result'),
                       url(r'usertasks/$', UserTasks.as_view(), name='queue-user-tasks'),
                       url(r'memcache',flushMemcache.as_view(), name= 'flush-memcache'),
                       url(r'^$', Queue.as_view(), name="queue-main"),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['api', 'json', 'jsonp', 'xml', 'yaml'])
