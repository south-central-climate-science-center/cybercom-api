from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from api import config

class CatalogPermission(permissions.BasePermission):
    """
    DataStore Detail View Permissions.
    SAFE_METHODS always TRUE
    UNSAFE need appropriate Permissions
    """
    def __init__(self,anonymous=config.CATALOG_ANONYMOUS):
        self.anonymous = anonymous
    def has_permission(self, request, view):

        django_app = 'catalog'
        admin_perm = 'catalog.catalog_admin'
        path = request.path.split('/')
        database = path[path.index(django_app)+2]
        collection = path[path.index(django_app)+3]
        perms=list(request.user.get_all_permissions())
        if request.method in permissions.SAFE_METHODS:
            code_perm= "{0}.{1}_{2}_{3}".format(django_app,database,collection,'safe')
            print perms, admin_perm,code_perm
            if self.anonymous or admin_perm in perms or code_perm in perms:
                print "shit"
                return True
            else:
                return False
        else:
            code_perm= "{0}.{1}_{2}_{3}".format(django_app,database,collection,request.method.lower())
            if request.user.is_superuser or admin_perm in perms or code_perm in perms:
                return True
            else:
                return False
class createCatalogPermission(permissions.BasePermission):
    """
    Create Database and Collections permissions.
    """

    def has_permission(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            django_app = 'catalog'
            admin_perm = 'catalog.catalog_admin'
            #Control catalog names per api_config
            path=request.path.split('/')
            if len(path)-path.index(django_app)==2:
                return False 
            perms=list(request.user.get_all_permissions())
            if request.user.is_superuser or admin_perm in perms: #or code_perm in perms:
                return True
            else:
                return False

