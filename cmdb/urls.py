#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views, api

app_name = 'cmdb'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^cmdb', views.cmdb, name='cmdb'),
    url(r'^index3', views.index3, name='index3'),
    url(r'^excel', views.excel, name='excel'),
    url(r'^login', views.login, name='login'),
    url(r'^collect', api.collect, name='update api'),
    #url(r'^api/gethostsjson', api.gethostsjson, name='gethostsjson'),
    url(r'^api/host', api.get_host, name='get_host'),
    url(r'^api/group', api.get_group, name='get_group'),
]