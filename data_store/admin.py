from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
# Register your models here.
from api import config
from models import dataStore
from pymongo import MongoClient

def setpermissions(app_label,model,codename,name):
    ct=ContentType.objects.get(app_label=app_label)
    Permission.objects.get_or_create(codename=codename, name=name, content_type=ct)

#data Store Permissions
db = MongoClient(host=config.DATA_STORE_MONGO_URI)
for database in db.database_names():
    if not (database in config.DATA_STORE_EXCLUDE):
        for col in db[database].collection_names():
            codename= "edit_{0}_{1}".format(database,col)
            name = "Edit {0} {1}".format(database,col)
            setpermissions('data_store',dataStore,codename,name)
