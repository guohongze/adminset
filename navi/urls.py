#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views

#app_name = 'navi'
urlpatterns = [
    url(r'^$', views.index, name='navi'),
    url(r'^add/', views.add, name='add'),
    url(r'^manage/', views.manage, name='manage'),
]