from django.shortcuts import render
from rest_framework_mongoengine import generics
from .models import catalogModel
from rest_framework.parsers import JSONParser

from .permission import catalogPermission,createCatalogPermission

from data_store.views import MongoDataStore, DataStore, DataStoreDetail
from api import config

class Catalog(MongoDataStore):
    permission_classes = (createCatalogPermission,)
    connect_uri = config.CATALOG_URI
    model = catalogModel
    view_reverse='catalog'
    exclude = config.CATALOG_EXCLUDE
    include = config.CATALOG_INCLUDE
    name = "include"

class CatalogData(DataStore, generics.ListCreateAPIView):
    permission_classes = (catalogPermission,)
    model = catalogModel
    connect_uri = config.CATALOG_URI

class CatalogDataDetail(DataStoreDetail):
    model = catalogModel
    connect_uri = config.CATALOG_URI
