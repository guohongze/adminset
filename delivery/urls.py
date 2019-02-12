#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from delivery import deli, tasks
urlpatterns = [
    url(r'^deliadd/$', deli.delivery_add, name='delivery_add'),
    url(r'^delilist/$', deli.delivery_list, name='delivery_list'),
    url(r'^delistatus/(?P<project_id>\d+)/$', deli.status, name='delivery_status'),
    url(r'^deliedit/(?P<project_id>\d+)/$', deli.delivery_edit, name='delivery_edit'),
    url(r'^delilog/(?P<project_id>\d+)/$', deli.log, name='delivery_log'),
    url(r'^delilog2/(?P<project_id>\d+)/$', deli.log2, name='delivery_log2'),
    url(r'^delilogdel/$', deli.log_del, name='log_del'),
    url(r'^delilogdelall/$', deli.log_delall, name='log_delall'),
    url(r'^delilogshistory/(?P<project_id>\d+)/$', deli.logs_history, name='logs_history'),
    url(r'^deligetlogs/(?P<project_id>\d+)/(?P<logname>.+)/$', deli.get_log, name='get_log'),
    url(r'^delideploy/(?P<project_id>\d+)/$', deli.delivery_deploy, name='delivery_deploy'),
    url(r'^delitaskstop/(?P<project_id>\d+)/$', deli.task_stop, name='delivery_taskstop'),
    url(r'^delidel/$', deli.delivery_del, name='delivery_del'),
]
