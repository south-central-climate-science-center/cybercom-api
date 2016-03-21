FROM python:2.7-onbuild
MAINTAINER Mark Stacy <markstacy@ou.edu>
RUN apt-get update && apt-get install -y vim  
EXPOSE 8080
CMD ["gunicorn", "--config=gunicorn.py", "--error-logfile=/data/api_log/api.log","--log-level=info", "api.wsgi:application"]
