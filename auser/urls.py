#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from auser import views


urlpatterns = [
    url(r'^$', views.index, name='auser'),
    url(r'^login/', views.login, name='login'),
    url(r'^login_out/', views.login_out, name='login_out'),
]