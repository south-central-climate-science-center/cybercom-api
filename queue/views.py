# Create your views here.
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly,DjangoModelPermissionsOrAnonReadOnly
from rest_framework.views import APIView
from ccelery.q import QueueTask, list_tasks, task_docstring
from models import Run_model
from rest_framework.renderers import JSONRenderer, JSONPRenderer
from renderer import QueueRunBrowsableAPIRenderer
from rest_framework.parsers import JSONParser
from util import trim

#task = list_tasks()['available_tasks']

q = QueueTask()


class Queue(APIView):
    permission_classes = ( IsAuthenticatedOrReadOnly,)

    def __init__(self,q=q, *args, **kwargs):
        self.q = q #QueueTask()
        self.task = self.q.list()['available_tasks']
        self.task_list = None
        super(Queue, self).__init__(*args, **kwargs)

    def get(self, request,format=None):
        if not self.task_list:
            self.task_list = []
            for task in self.task:
                self.task_list.append(reverse('run-main',kwargs={'task_name':task},request=request))
                #self.task_list.append(reverse('%s-run' % task, request=request))
        return Response({
            'Tasks': self.task_list,
            'Task History': reverse('queue-user-tasks',request=request)
        })


class Run(APIView):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    model = Run_model
    parser_classes = (JSONParser,)
    renderer_classes = (QueueRunBrowsableAPIRenderer, JSONRenderer, JSONPRenderer,)

    def __init__(self,q=q, *args, **kwargs):
        self.q = q #QueueTask()
        self.tasks_queues = self.q.list()
        # self.task = self.q.list()['available_tasks']
        # self.task_list = None
        super(Run, self).__init__(*args, **kwargs)

    def get_username(self, request):
        username = "guest"
        if request.user.is_authenticated():
            username = request.user.username
        return username

    def get(self, request,task_name=None,format=None):
        #task_name = filter(None, request._request.path.split('/'))[-1]
        docstring = trim(task_docstring(task_name))
        curl_url = reverse('run-main',kwargs={'task_name':task_name},request=request)
        #reverse("%s-run" % (task_name), request=request)
        data = {'task_name': task_name, 'task_docstring': docstring, 'task_url': curl_url, 'queue': 'celery'}
        return Response(data)

    def post(self, request,task_name=None,format=None):
        if not task_name:
            task_name = request.DATA.get('function', None)
        if task_name not in self.tasks_queues['available_tasks']:
            raise Exception("%s Task is not available" % (task_name))
        queue = request.DATA.get('queue', 'celery')
        if queue not in self.tasks_queues['available_queues']:
            raise Exception("%s Queue is not available" % (queue))
        args = request.DATA.get('args', [])
        kwargs = request.DATA.get('kwargs', {})
        result = self.q.run(task_name, args, kwargs, queue, self.get_username(request))
        result['result_url']=reverse('queue-task-result', kwargs={'task_id':result['task_id']}, request=request)
        return Response(result)


class UserResult(APIView):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    model = Run_model
    parser_classes = (JSONParser,)

    def __init__(self,q=q, *args, **kwargs):
        self.q = q #QueueTask()
        super(UserResult, self).__init__(*args, **kwargs)

    def get(self, request, task_id=None,format=None):
        if task_id:
            try:
                data = self.q.task(task_id)
            except Exception as inst:
                data = {'task_id': task_id, 'error': inst.message}
            return Response(data)


class UserTasks(APIView):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    model = Run_model

    def __init__(self,q=q, *args, **kwargs):
        self.q = q #QueueTask()
        self.task = self.q.list()['available_tasks']
        self.task_list = None
        # self.mongo_encoder = MongoEncoder()
        super(UserTasks, self).__init__(*args, **kwargs)

    def get_username(self, request):
        username = "guest"
        if request.user.is_authenticated():
            username = request.user.username
        return username

    def get(self, request,format=None):
        result = {'count': 0, 'next': None, 'previous': None, 'results': []}
        page_parm = api_settings.user_settings.get('PAGINATE_BY_PARAM', 'page_size')
        if page_parm in request.GET:
            limit = request.GET.get(page_parm, 10)
        else:
            limit = api_settings.user_settings.get('PAGINATE_BY', 10)
        # Set page to 1 or page GET
        page = request.GET.get('page', 1)
        try:
            page = int(page)
        except:
            page = 1
        task_name = request.GET.get('taskname', None)
        username = self.get_username(request)
        data = self.q.history(username, task_name=task_name, page=page, limit=limit,request=request)
        #for item in data:


        # data['next']= reverse('queue-user-tasks',kwargs={'page':page+1,},request=request)
        # if isinstance(data,ObjectId):
        # return str(obj)
        #print data
        return Response(data)  #,indent=4,sort_keys=True))


"""
  # print task_docstring(task_name)
        html ="<div class='div_help'><b>Task Name: %s<br>Task Docstring:</b><code>%s</code>Example Curl:<br>%s</div>"
        baseHelp =""curl --data-ascii '{ "function": "%s",
         "queue": "%s",
          "args": [],
          "kwargs": {}
          }' %s -H Content-Type:application/json"" % (task_name,"celery",reverse("%s-run" % (task_name), request=request))
        html = html % (task_name,task_docstring(task_name),baseHelp)
        #html = html % (task_name,markdown.markdown(trim(task_docstring(task_name))),baseHelp)
        return Response(html) #, template_name='rest_framework/queue_run_api.html')



from json import JSONEncoder
from bson.objectid import ObjectId

class MongoEncoder(JSONEncoder):
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return JSONEncoder.default(obj, **kwargs)


    from rest_framework.renderers import JSONRenderer, JSONPRenderer
from rest_framework import renderers
import json

class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return data.encode(self.charset)


"""
