#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import system
import api


urlpatterns = [
    url(r'^system/$', system.index, name='monitor'),
    url(r'^system/(?P<hostname>.+)/(?P<timing>\d+)/$', system.host_info, name='host_info'),
    url(r'^get/cpu/(?P<hostname>.+)/(?P<timing>\d+)/$', system.get_cpu, name='get_cpu'),
    url(r'^get/mem/(?P<hostname>.+)/(?P<timing>\d+)/$', system.get_mem, name='get_mem'),
    url(r'^get/disk/(?P<hostname>.+)/(?P<timing>\d+)/(?P<partition>\d+)/$', system.get_disk, name='get_disk'),
    url(r'^get/net/(?P<hostname>.+)/(?P<timing>\d+)/(?P<net_id>\d+)/$', system.get_net, name='get_net'),
    url(r'^received/sys/info/$', api.received_sys_info, name='received_sys_info'),
]