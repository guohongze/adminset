#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from delivery import deli, tasks
urlpatterns = [
    url(r'^$', deli.delivery_list, name='delivery'),
    url(r'^add/$', deli.delivery_add, name='delivery_add'),
    url(r'^ist/$', deli.delivery_list, name='delivery_list'),
    url(r'^status/(?P<project_id>\d+)/$', deli.status, name='delivery_status'),
    url(r'^edit/(?P<project_id>\d+)/$', deli.delivery_edit, name='delivery_edit'),
    url(r'^log/(?P<project_id>\d+)/$', deli.log, name='delivery_log'),
    url(r'^log2/(?P<project_id>\d+)/$', deli.log2, name='delivery_log2'),
    url(r'^deploy/(?P<project_id>\d+)/$', deli.delivery_deploy, name='delivery_deploy'),
    url(r'^taskstop/(?P<project_id>\d+)/$', deli.task_stop, name='delivery_taskstop'),
    url(r'^delete/$', deli.delivery_del, name='delivery_del'),
]
