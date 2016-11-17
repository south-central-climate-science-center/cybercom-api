from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from itertools import chain

class dataStorePermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

    def has_permission(self, request, view):
        perms=list(request.user.get_all_permissions()) 
        for itm in perms:
            print itm
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            django_app = 'data_store'
            admin_perm = 'data_store.datastore_admin'
            path = request.path
            path=path.split('/')
            code_perm= "{0}.edit_{1}_{2}".format(django_app,path[-3],path[-2])
            #if request.resolver_match.app_name == 'data_store':
            #    admin_perm = 'data_store.datastore_admin'
            #else:
            #    admin_perm = 'catalog.catalog_admin'
            perms=list(request.user.get_all_permissions())
            if request.user.is_superuser or admin_perm in perms or code_perm in perms:
                return True
            else:
                return False 

"""
    def get_user_permissions(self,user):
        if user.is_superuser:
            return Permission.objects.all()
        return user.user_permissions.all() | Permission.objects.filter(group__user=user)

#list(set(chain(user.user_permissions.filter(content_type=ctype).values_list('codename', flat=True), Permission.objects.filter(group__user=user, content_type=ctype).values_list('codename', flat=True))))

"""
