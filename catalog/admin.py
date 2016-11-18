from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
# Register your models here.
from api import config
from models import catalogModel
from pymongo import MongoClient

def setpermissions(app_label,model,codename,name):
    ct = ContentType.objects.get_for_model(catalogModel)
    #ct=ContentType.objects.get(app_label=app_label)
    Permission.objects.get_or_create(codename=codename, name=name, content_type=ct)

#Catalog Permissions
db = MongoClient(host=config.CATALOG_URI)
for catalog in config.CATALOG_INCLUDE:
    for col in db[catalog].collection_names():
        codename= "edit_{0}_{1}".format(catalog,col)
        name = "Edit {0} {1}".format(catalog,col)
        setpermissions('catalog','catalogModel',codename,name)

