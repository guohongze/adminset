#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from config import views


urlpatterns = [
    url(r'^$', views.index, name='config'),
    url(r'^config_save/$', views.config_save, name='config_save'),
    url(r'^token/', views.get_token, name='token'),
]