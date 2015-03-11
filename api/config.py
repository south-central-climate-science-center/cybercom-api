__author__ = 'mstacy'

#****** Application Settings *******************************************************
Page_Title = 'API'
Application_Title = 'Django Rest Cybercommons'
#****** Django Settings  ***********************************************************

SECRET_KEY = 'l-+nq5_8go-037rjvwb4a9nn6h2otbu@1ap0v49qg(#9l=l&*)'
# SCRIPT_NAME Override, I had difficulty setting up NGINX settings
# proxy_set_header SCRIPT_NAME /api; # Not working in config. Temporary fix by add 
# FORCE_SCRIPT_NAME in Django settings.py 
# If None will default back to Nginx config. 
# Provide custom config.py with docker cybercom/api
# docker run -v <path to config.py>:/usr/src/app/api/config.py cybercom/api
FORCE_SCRIPT_NAME=None

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
# Cookie Domain
# Domain cookie. Can overide for subdomains ie. ".example.com"  (note the leading dot!) 
# for cross-domain cookies, or use None for a standard domain cookie.
SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_DOMAIN = None

#******* Queue  *******************************************************

MEMCACHE_HOST = "127.0.0.1"
MEMCACHE_PORT = 11211

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = "mgmic_queue"
MONGO_LOG_COLLECTION = "mgmic_task_log"
MONGO_TOMBSTONE_COLLECTION = "mgmic_tombstone"

BROKER_URL = 'pyamqp://mgmic:mgm1cpass@localhost:5672/mgmic'

CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": MONGO_HOST,
    "database": MONGO_DB,
    "taskmeta_collection": MONGO_TOMBSTONE_COLLECTION
}

#******* Catalog ******************************************************
CATALOG_EXCLUDE = ['admin','local','cybercom_auth','system.users']
CATALOG_URI = 'mongodb://localhost:27017/'

#*********** Data Store ************************************************
DATA_STORE_EXCLUDE = ['admin','local','cybercom_auth','system.users','cybercom_queue','df']
DATA_STORE_MONGO_URI = 'mongodb://localhost:27017/'
