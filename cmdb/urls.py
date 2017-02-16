#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from cmdb import views, api


urlpatterns = [
    #url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.cmdb_index, name='cmdb'),
    url(r'^excel/', views.excel, name='excel'),
    url(r'^asset_add/', views.asset_add, name='asset_add'),
    url(r'^asset_del/', views.asset_del, name='asset_del'),
    url(r'^asset_edit/', views.asset_edit, name='asset_edit'),
    url(r'^asset_save/', views.asset_save, name='asset_save'),
    url(r'^idc_add/', views.idc_add, name='idc_add'),
    url(r'^login', views.login, name='login'),
    url(r'^sync', views.hostsync, name='sync'),
    url(r'^collect', api.collect, name='update_api'),
    url(r'^api/host', api.get_host, name='get_host'),
    url(r'^api/group', api.get_group, name='get_group'),
]