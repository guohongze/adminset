#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views, api

app_name = 'cmdb'
urlpatterns = [
    #url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.cmdb, name='cmdb'),
    url(r'^excel', views.excel, name='excel'),
    url(r'^login', views.login, name='login'),
    url(r'^sync', views.hostsync, name='sync'),
    url(r'^collect', api.collect, name='update_api'),
    url(r'^api/host', api.get_host, name='get_host'),
    url(r'^api/group', api.get_group, name='get_group'),
]