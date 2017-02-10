#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views

app_name = 'cmdb'
urlpatterns = [
    url(r'^$', views.ansible, name='ansible'),
    url(r'^exec', views.ansiblexe, name='exec'),
]