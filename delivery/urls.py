#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
import delivery
#import tasks
urlpatterns = [
    url(r'^$', delivery.delivery_list, name='delivery'),
    url(r'^add/$', delivery.delivery_add, name='delivery_add'),
    url(r'^ist/$', delivery.delivery_list, name='delivery_list'),
    url(r'^status/(?P<project_id>\d+)/$', delivery.status, name='delivery_status'),
    url(r'^edit/(?P<project_id>\d+)/$', delivery.delivery_edit, name='delivery_edit'),
    url(r'^log/(?P<project_id>\d+)/$', delivery.log, name='delivery_log'),
    url(r'^log2/(?P<project_id>\d+)/$', delivery.log2, name='delivery_log2'),
    url(r'^deploy/(?P<project_id>\d+)/$', delivery.delivery_deploy, name='delivery_deploy'),
    url(r'^taskstop/(?P<project_id>\d+)/$', delivery.task_stop, name='delivery_taskstop'),
    url(r'^delete/$', delivery.delivery_del, name='delivery_del'),
]
