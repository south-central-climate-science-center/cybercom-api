#from cybercom_queue.ccelery import config
from api import config

import ssl

BROKER_URL = config.BROKER_URL
BROKER_USE_SSL = config.BROKER_USE_SSL

#BROKER_URL = 'amqp://quser:qpass@cybercom_rabbitmq:5671/vhost'
#BROKER_USE_SSL = {
#  'keyfile': '/sslconf/client/key.pem',
#  'certfile': '/sslconf/client/cert.pem',
#  'ca_certs': '/sslconf/testca/cacert.pem',
#  'cert_reqs': ssl.CERT_REQUIRED
#}

CELERY_SEND_EVENTS = True
CELERY_TASK_RESULT_EXPIRES = None

CELERY_RESULT_BACKEND = config.CELERY_RESULT_BACKEND

CELERY_MONGODB_BACKEND_SETTINGS = config.CELERY_MONGODB_BACKEND_SETTINGS 

