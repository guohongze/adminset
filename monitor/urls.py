#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views
import api


urlpatterns = [
    url(r'^system/$', views.index, name='monitor'),
    url(r'^system/(?P<hostname>.+)/(?P<timing>\d+)/$', views.host_info, name='host_info'),
    url(r'^get/cpu/(?P<hostname>.+)/(?P<timing>\d+)/$', views.get_cpu, name='get_cpu'),
    url(r'^get/mem/(?P<hostname>.+)/(?P<timing>\d+)/$', views.get_mem, name='get_mem'),
    url(r'^get/disk/(?P<hostname>.+)/(?P<timing>\d+)/(?P<partition>\d+)/$', views.get_disk, name='get_disk'),
    url(r'^received/sys/info/$', api.received_sys_info, name='received_sys_info'),
]