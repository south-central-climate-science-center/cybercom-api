__author__ = 'mstacy'
from rest_framework.permissions import DjangoModelPermissions


class DjangoMongoPermissionsOrAnonReadOnly(DjangoModelPermissions):
    """
    Similar to DjangoModelPermissions, except that anonymous users are
    allowed read-only access.
    """

    authenticated_users_only = False

    def get_required_permissions(self, method, model_cls):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """
        try:
            appLabel = model_cls._meta.app_label
        except:
            #added for mongoengine
            appLabel = model_cls._meta['app_label']
        try:
            modelName = get_model_name(model_cls)
        except:
            #add for mongoengine
            modelName = model_cls._meta['model_name']
        kwargs = {
            'app_label': appLabel,
            'model_name': modelName
        }
        return [perm % kwargs for perm in self.perms_map[method]]