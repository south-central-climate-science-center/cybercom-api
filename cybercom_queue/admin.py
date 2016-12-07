from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
# Register your models here.
from api import config
from models import taskModel

# Register your models here.
def setpermissions(app_label,codename,name):
    try:
        ct = ContentType.objects.get_for_model(taskModel)
        Permission.objects.get_or_create(codename=codename, name=name, content_type=ct)
    except:
         print("Unable to create {0} permission.".format(codename))


#create admin permissions
setpermissions('cybercom_queue','task_admin',"Task Admin")
