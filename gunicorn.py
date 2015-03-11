# gunicorn.py
import multiprocessing
import os

if os.environ.get('MODE') == 'dev':
    reload = True

bind = '0.0.0.0:8080'

workers = multiprocessing.cpu_count() * 2 + 1
