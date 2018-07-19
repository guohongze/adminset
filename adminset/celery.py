#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
try:
    import configparser as cf
except Exception as msg:
    print(msg)
    import ConfigParser as cf

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminset.settings')
app = Celery('adminset')

# redis connect code
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = cf.ConfigParser()
config.read(os.path.join(BASE_DIR, 'adminset.conf'))
redis_host = config.get('redis', "redis_host")
redis_port = config.get("redis", "redis_port")
redis_db = config.get('redis', "redis_db")
redis_password = config.get('redis', "redis_password")
if redis_password:
    app.conf.broker_url = 'redis://:{0}@{1}:{2}/{3}'.format(redis_password, redis_host, redis_port, redis_db)
else:
    app.conf.broker_url = 'redis://{0}:{1}/{2}'.format(redis_host, redis_port, redis_db)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))