#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from cmdb import views, api, idc, asset


urlpatterns = [
    url(r'^$', views.cmdb_index, name='cmdb'),
    url(r'^asset_add/', asset.asset_add, name='asset_add'),
    url(r'^asset_del/', asset.asset_del, name='asset_del'),
    url(r'^asset_edit/', asset.asset_edit, name='asset_edit'),
    url(r'^asset_save/', asset.asset_save, name='asset_save'),
    url(r'^idc/', idc.idc, name='idc'),
    url(r'^idc_add/', idc.idc_add, name='idc_add'),
    url(r'^idc_add_mini/', idc.idc_add_mini, name='idc_add_mini'),
    url(r'^idc_del/', idc.idc_del, name='idc_del'),
    url(r'^idc_save/', idc.idc_save, name='idc_save'),
    url(r'^idc_edit/', idc.idc_edit, name='idc_edit'),
    url(r'^login', views.login, name='login'),
    url(r'^excel/', views.excel, name='excel'),
    url(r'^sync', views.hostsync, name='sync'),
    url(r'^collect', api.collect, name='update_api'),
    url(r'^api/host', api.get_host, name='get_host'),
    url(r'^api/group', api.get_group, name='get_group'),
]