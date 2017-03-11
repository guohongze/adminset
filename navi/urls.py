#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from navi import views

urlpatterns = [
    url(r'^$', views.index, name='navi'),
    url(r'^add/', views.add, name='add'),
    url(r'^manage/', views.manage, name='manage'),
    url(r'^delete/', views.delete, name='delete'),
    url(r'^edit/', views.edit, name='edit'),
    url(r'^save/', views.save, name='save'),
]