"""
Django settings for ows_api project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from api import config

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)
#print TEMPLATE_DIRS
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "api.processor.title",
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.SECRET_KEY

FORCE_SCRIPT_NAME = config.FORCE_SCRIPT_NAME
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.DEBUG

TEMPLATE_DEBUG = config.TEMPLATE_DEBUG

ALLOWED_HOSTS = config.ALLOWED_HOSTS

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'catalog.permission.DjangoMongoPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    #Renderer defaults
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
        # UJSON 2.3 times faster then std json renderer
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.JSONPRenderer',
        'rest_framework.renderers.XMLRenderer',
        'rest_framework.renderers.YAMLRenderer',
        #'data_layer.pagination.PaginatedCSVRenderer',
        #'drf_ujson.renderers.UJSONRenderer',

    ),
    #Pagination settings
    'PAGINATE_BY': 50,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 1000000,
    'Page_Title': config.Page_Title ,
    'Application_Title': config.Application_Title

}

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'cybercom_queue',
    'catalog',
    'data_store'

)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

)

ROOT_URLCONF = 'api.urls'

WSGI_APPLICATION = 'api.wsgi.application'

# Database
DATABASES = config.DATABASES

DATABASE_ROUTERS = config.DATABASE_ROUTERS

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static/api"),)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
#STATIC_ROOT = os.path.join(BASE_DIR, "static/api") #"/var/www/example.com/static/"
#print STATIC_ROOT
STATIC_URL = '/static/api/'
#templates
#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.load_template_source',
#    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
#)
SESSION_COOKIE_DOMAIN = config.SESSION_COOKIE_DOMAIN
CSRF_COOKIE_DOMAIN = config.CSRF_COOKIE_DOMAIN
base = ''
if FORCE_SCRIPT_NAME:
    if FORCE_SCRIPT_NAME[-1]=='/':
        base=FORCE_SCRIPT_NAME[:-1]
    else:
        base=FORCE_SCRIPT_NAME
    LOGIN_REDIRECT_URL ="%s/" % (base)
    LOGIN_URL="%s/api-auth/login/" % (base)
else:
    base=''
    LOGIN_REDIRECT_URL ="%s/" % (base)
    LOGIN_URL="%s/api-auth/login/" % (base)
