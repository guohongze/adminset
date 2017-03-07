#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from accounts import views


urlpatterns = [
    url(r'^$', views.index, name='accounts'),
    url(r'^login/$', views.login, name='loginurl'),
    url(r'^loginout/$', views.loginout, name='loginout'),
]