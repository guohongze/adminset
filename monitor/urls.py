#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views
import api


urlpatterns = [
    url(r'^system/$', views.index, name='monitor'),
    url(r'^system/(?P<hostname>.+)/$', views.host_info, name='host_info'),
    url(r'^get/data/(?P<hostname>.+)/$', views.get_sys_data, name='get_sys_data'),
    url(r'^received/sys/info/$', api.received_sys_info, name='received_sys_info'),
]