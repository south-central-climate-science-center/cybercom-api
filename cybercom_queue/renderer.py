__author__ = 'mstacy'
from rest_framework.renderers import BrowsableAPIRenderer
from django import forms

class QueueRunBrowsableAPIRenderer(BrowsableAPIRenderer):
    #def get_default_renderer(self, view):
    #    return JSONRenderer()

    template = 'rest_framework/queue_run_api.html'
    def get_context(self, data, accepted_media_type, renderer_context):
        context= super(QueueRunBrowsableAPIRenderer,self).get_context(data, accepted_media_type, renderer_context)
        if context['request'].method.upper() == 'GET':
            #context['raw_data_post_form'].data = {"_content":"test"}
            context['content']=data
        return context