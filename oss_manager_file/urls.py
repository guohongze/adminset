#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^get_file', views.get_file, name='get_file'),
    url(r'^path_create', views.path_create, name='path_create'),
    url(r'^upload_file', views.upload_file, name='upload_file'),
]