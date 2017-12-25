#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
import delivery
import tasks
urlpatterns = [
    url(r'^$', delivery.delivery_list, name='delivery'),
    url(r'^delivery/add/$', delivery.delivery_add, name='delivery_add'),
    url(r'^delivery/list/$', delivery.delivery_list, name='delivery_list'),
    url(r'^delivery/edit/(?P<project_id>\d+)/$', delivery.delivery_edit, name='delivery_edit'),
    url(r'^delivery/log/(?P<project_id>\d+)/$', delivery.log, name='delivery_log'),
    url(r'^delivery/deploy/(?P<project_id>\d+)/$', delivery.delivery_deploy, name='delivery_deploy'),
    url(r'^delivery/delete/$', delivery.delivery_del, name='delivery_del'),
]
