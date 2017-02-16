#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from navi import views

#app_name = 'navi'
urlpatterns = [
    url(r'^$', views.navi_index, name='navi'),
    url(r'^add/', views.add, name='add'),
    url(r'^manage/', views.manage, name='manage'),
    url(r'^delete/', views.delete, name='delete'),
    url(r'^edit/', views.edit, name='edit'),
    url(r'^save/', views.save, name='save'),
]