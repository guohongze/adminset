#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views, api

app_name = 'cmdb'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^index1', views.index1, name='index1'),
    url(r'^index2', views.index2, name='index2'),
    url(r'^index3', views.index3, name='index3'),
    url(r'^execl', views.execl, name='execl'),
    url(r'^login', views.login, name='login'),
    url(r'^collect', api.collect, name='update api'),
    url(r'^gett', api.gett, name='gett'),
    url(r'^geti', api.geti, name='geti'),
    url(r'^getj', api.getj, name='getj'),
]