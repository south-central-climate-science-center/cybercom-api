__author__ = 'mstacy'
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import serializers, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import AuthtokenToken
from django.contrib.auth.decorators import login_required

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)



class APIRoot(APIView):
    permission_classes = ( IsAuthenticatedOrReadOnly,)

    def get(self, request,format=None):
        # Assuming we have views named 'foo-view' and 'bar-view'
        # in our project's URLconf.
        return Response({
            'Queue': {'Tasks': reverse('queue-main', request=request),
                      'Tasks History': reverse('queue-user-tasks',request=request)},
            'Catalog': {'Data Source':reverse('catalog-list',request=request)},
            'Data Store': {'Mongo':reverse('data-list',request=request)},
            'User Profile': {'User':reverse('user-list',request=request)}
        })

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()

class UserProfile(LoginRequiredMixin,APIView):
    permission_classes = ( IsAuthenticated,)
    serializer_class = UserSerializer
    model = User
    def get(self,request,id=None,format=None):
        data = User.objects.get(pk=self.request.user.id)
        serializer = self.serializer_class(data,context={'request':request})
        tok = Token.objects.get_or_create(user=self.request.user)
        data = serializer.data
        data['auth-token']= str(tok[0])
        return Response(data)

from rest_framework import permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
