#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from delivery import deli, tasks
urlpatterns = [
    url(r'^$', deli.delivery_list, name='delivery'),
    url(r'^add/$', deli.delivery_add, name='delivery_add'),
    url(r'^list/$', deli.delivery_list, name='delivery_list'),
    url(r'^status/(?P<project_id>\d+)/$', deli.status, name='delivery_status'),
    url(r'^edit/(?P<project_id>\d+)/$', deli.delivery_edit, name='delivery_edit'),
    url(r'^log/(?P<project_id>\d+)/$', deli.log, name='delivery_log'),
    url(r'^log2/(?P<project_id>\d+)/$', deli.log2, name='delivery_log2'),
    url(r'^log/delete/$', deli.log_del, name='log_del'),
    url(r'^log/delall/$', deli.log_delall, name='log_delall'),
    url(r'^logs/history/(?P<project_id>\d+)/$', deli.logs_history, name='logs_history'),
    url(r'^get/logs/(?P<project_id>\d+)/(?P<logname>.+)/$', deli.get_log, name='get_log'),
    url(r'^deploy/(?P<project_id>\d+)/$', deli.delivery_deploy, name='delivery_deploy'),
    url(r'^taskstop/(?P<project_id>\d+)/$', deli.task_stop, name='delivery_taskstop'),
    url(r'^delete/$', deli.delivery_del, name='delivery_del'),
]
