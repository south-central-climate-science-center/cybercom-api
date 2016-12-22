__author__ = 'mstacy'
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import serializers, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
#from .models import AuthtokenToken, AuthUser
from django.contrib.auth.decorators import login_required
from hashlib import md5
#from rest_framework import viewsets
#from rest_framework.permissions import AllowAny
#from .permissions import IsStaffOrTargetUser

#Login required mixin
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)



class APIRoot(APIView):
    permission_classes = ( IsAuthenticatedOrReadOnly,)

    def get(self, request,format=None):
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
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)

class UserProfile(LoginRequiredMixin,APIView):
    permission_classes = ( IsAuthenticated,)
    serializer_class = UserSerializer
    fields = ('username', 'first_name', 'last_name', 'email')
    model = User
    def get(self,request,id=None,format=None):
        data = User.objects.get(pk=self.request.user.id)
        serializer = self.serializer_class(data,context={'request':request})
        tok = Token.objects.get_or_create(user=self.request.user)
        rdata = serializer.data
        rdata['name'] = data.get_full_name() 
        rdata['gravator_url']="{0}://www.gravatar.com/avatar/{1}".format(request.scheme,md5(rdata['email'].strip(' \t\n\r')).hexdigest()) 
        rdata['auth-token']= str(tok[0])
        return Response(rdata)
    def post(self,request,format=None):
        user = User.objects.get(pk=self.request.user.id)
        password = request.DATA.get('password', None)
        if password:
            user.set_password(password)
            user.save()
            data = {"password":"Successfully Updated"}
            return Response(data)
        auth_tok  = request.DATA.get('auth-token', None)
        if str(auth_tok).lower()=="update":
            tok = Token.objects.get(user=user)    
            tok.delete()
            tok = Token.objects.get_or_create(user=self.request.user)
            data = {"auth-token":str(tok[0])}
            return Response(data)
        else:
            user.first_name =request.DATA.get('first_name', user.first_name)
            user.last_name = request.DATA.get('last_name', user.last_name)
            user.email = request.DATA.get('email', user.email)
            serializer = self.serializer_class(user,context={'request':request})
            data = serializer.data
            user.save()
            tok = Token.objects.get_or_create(user=self.request.user)
            data['name'] = user.get_full_name()
            data['gravator_url']="{0}://www.gravatar.com/avatar/{1}".format(request.scheme,md5(data['email'].strip(' \t\n\r')).hexdigest())
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
