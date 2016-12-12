# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from pymongo import MongoClient
from api import config
from .models import dataStore
# Create your views here.
from rest_framework.settings import api_settings
from .mongo_paginator import MongoDataPagination, MongoDistinct,MongoGroupby, MongoDataGet,MongoDataDelete,MongoDataSave,MongoDataInsert
from .renderer import DataBrowsableAPIRenderer, mongoJSONPRenderer,mongoJSONRenderer
from rest_framework.renderers import XMLRenderer, YAMLRenderer,JSONPRenderer
from rest_framework.parsers import JSONParser
from permission import  DataStorePermission, createDataStorePermission
 
class MongoDataStore(APIView):
    permission_classes = ( createDataStorePermission,)
    renderer_classes = (DataBrowsableAPIRenderer, mongoJSONRenderer, mongoJSONPRenderer, XMLRenderer, YAMLRenderer)
    title = "Database"
    parser_classes = (JSONParser,)
    connect_uri = config.DATA_STORE_MONGO_URI
    view_reverse='data'
    name = "exclude"
    exclude= config.DATA_STORE_EXCLUDE
    def __init__(self):
        self.db = MongoClient(host=self.connect_uri)
    def get(self, request, database=None, format=None):
        #self.db = MongoClient(host=self.connect_uri)
        urls = []
        if database:
            self.title = "Collection"
            data = list(self.db[database].collection_names())
            #print data
            data.sort()
            for col in data:
                if "%s.%s" % (database,col) in self.exclude or col in self.exclude:
                    pass
                else:
                    urls.append(reverse("%s-detail" % (self.view_reverse), kwargs={'database': database, 'collection': col}, request=request))
            return Response({'Database': database, 'Available Collections': urls})
        else:
            self.title = "Database"
            data = list(self.db.database_names())
            data.sort()
            #This section used for catalog django app
            if self.name == "include":
                data = self.include

            for db in data:
                if db in self.exclude:
                    pass
                else:
                    urls.append(reverse("%s-list"% (self.view_reverse), kwargs={'database': db}, request=request))
            return Response({
                'Available Databases': urls})
    def post(self,request,database=None,format=None):
            #Action Delete
            action=request.DATA.get('action', '')
            collection=request.DATA.get('collection', None)
            if action.lower()=='delete':
                print(config.FORCE_SCRIPT_NAME)
                try:
                    shift_url = len(config.FORCE_SCRIPT_NAME.split('/'))
                    print shift_url
                    if shift_url>1:
                        shift=shift_url -3
                    else:
                        shift=-1
                except:
                    shift =-1
                if database:
                    if len(request.path.split('/'))==5+shift:
                        try:
                            self.db.drop_database(database)
                            return Response({database:"Deleted"})
                        except Exception as e:
                            return Response({"Error":str(e)})
                    else:
                        return Response({"ERROR":"Must be on Database View to drop database."})
                elif collection:
                    if len(request.path.split('/'))==6+shift:
                        try:
                            self.db.drop_collection(collection)
                            return Response({collection:"Deleted"})
                        except Exception as e:
                            return Response({"Error":str(e)})
                    else:
                        return Response({"ERROR":"Must be on Collection View to drop collection."})
                else:
                    return Response({"ERROR":"Database {0} Collection {1} Action {2}".format(database,collection,action)})
            #Action Create (default None)
            if database:
                col=request.DATA.get('collection', None)
                if col:
                    data = request.DATA.get('data', {})
                    self.db[database][col].insert_one(data)
                    self.db[database][col].remove({})
                    return Response({'database':database,'collection':col})
                else:
                    return Response({'ERROR':"Must submit 'collection' name as part of post"})
            else:
                data = request.DATA.get('database', None)
                if data:
                    self.db[data]['default_collection'].insert_one({})
                    return Response({'database':data})
                else:
                    return Response({'ERROR':"Must submit 'database' name as part of post"})


class DataStore(APIView):
    permission_classes = (DataStorePermission,) #DjangoModelPermissionsOrAnonReadOnly,)
    model = dataStore 
    renderer_classes = (DataBrowsableAPIRenderer, mongoJSONRenderer, mongoJSONPRenderer, XMLRenderer, YAMLRenderer)
    parser_classes = (JSONParser,)
    connect_uri = config.DATA_STORE_MONGO_URI
    def __init__(self):
        self.db = MongoClient(host=self.connect_uri)

    def get(self, request, database=None, collection=None, format=None):
        #self.db = MongoClient(host=self.connect_uri)
        #print self.connect_uri
        query = request.QUERY_PARAMS.get('query', None)
        page_size = request.QUERY_PARAMS.get(api_settings.user_settings.get('PAGINATE_BY_PARAM', 'page_size'),
                                             api_settings.user_settings.get('PAGINATE_BY', 10))
        try:
            page = int(request.QUERY_PARAMS.get('page', 1))
        except:
            page = 1
        try:
            page_size = int(page_size)
        except:
            page_size = int(api_settings.user_settings.get('PAGINATE_BY', 10))

        url = request and request.build_absolute_uri() or ''
        action = request.QUERY_PARAMS.get('action','None')
        if action.lower()=="distinct":
            field = request.QUERY_PARAMS.get('field',None)
            if field:
                data = MongoDistinct(field,self.db, database, collection, query=query)
            else:
                data = {"ERROR":"Must provide keyword field to perform distinct operation."}
        elif action.lower()=="groupby":
            variable = request.QUERY_PARAMS.get('variable',None)
            if not variable:
                data = {"ERROR":"Must provide keyword field to perform aggregation operation."}
            groupby=request.QUERY_PARAMS.get('groupby',None)
            if groupby:
                gbs=groupby.split(',')
                data = MongoGroupby(variable,gbs,self.db, database, collection, query=query)
            else:
                data = {"ERROR":"Must provide groupby column names. Multiple separate by comma."}
        else:
            data = MongoDataPagination(self.db, database, collection, query=query, page=page, nPerPage=page_size, uri=url)
        return Response(data)
    def post(self,request,database=None,collection=None,format=None):
        result =MongoDataInsert(self.db, database, collection,request.DATA)
        return Response(result)

class DataStoreDetail(APIView):
    permission_classes = (DataStorePermission,) #DjangoModelPermissionsOrAnonReadOnly,)
    model = dataStore
    renderer_classes = (DataBrowsableAPIRenderer, mongoJSONRenderer, mongoJSONPRenderer, XMLRenderer, YAMLRenderer)
    parser_classes = (JSONParser,)
    connect_uri = config.DATA_STORE_MONGO_URI
    def __init__(self):
        self.db = MongoClient(host=self.connect_uri)
    def get(self,request,database=None, collection=None,id=None, format=None):
        data = MongoDataGet(self.db,database,collection,id)
        return Response(data)
    def put(self,request,database=None, collection=None,id=None, format=None):
        return Response(MongoDataSave(self.db,database,collection,id,request.DATA))
    def delete(self,request,database=None, collection=None,id=None, format=None):
        result = MongoDataDelete(self.db,database,collection,id)
        return Response({"deleted_count":result.deleted_count,"_id":id})
