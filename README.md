Cybercommons API Docker Build 
===
Django Rest API which includes Tasks, Catalog, Local Data Store


Docker api works in conjuction with docker cybercom/celery image.

First need to add config.py 

    wget -o config.py https://raw.githubusercontent.com/ouinformatics/ccstack-docker/master/api/api/config_example.py

Adjust config.py to your local configuration

Docker API commands

    docker run -d --net=host -v /path/to/config.py:/usr/src/app/api/config.py cybercom/api

This docker container export to localhost:8080
 
Can proxy with NGINX

Default User: admin
Default Password: admin
