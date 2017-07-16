#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from cmdb import api, idc, asset, group


urlpatterns = [
    url(r'asset/$', asset.asset, name='cmdb'),
    url(r'^asset/add/$', asset.asset_add, name='asset_add'),
    url(r'^asset/del/$', asset.asset_del, name='asset_del'),
    url(r'^asset/edit/(?P<ids>\d+)/$', asset.asset_edit, name='asset_edit'),
    # url(r'^asset/save/$', asset.asset_save, name='asset_save'),
    url(r'^group/$', group.group, name='group'),
    url(r'^group/del/$', group.group_del, name='group_del'),
    url(r'^group/add/$', group.group_add, name='group_add'),
    url(r'^group/edit/(?P<ids>\d+)/$', group.group_edit, name='group_edit'),
    url(r'^group/save/$', group.group_save, name='group_save'),
    url(r'^idc/$', idc.idc, name='idc'),
    url(r'^idc/add/$', idc.idc_add, name='idc_add'),
    url(r'^idc/del/$', idc.idc_del, name='idc_del'),
    url(r'^idc/save/$', idc.idc_save, name='idc_save'),
    url(r'^idc/edit/(?P<ids>\d+)/$', idc.idc_edit, name='idc_edit'),
    url(r'^collect', api.collect, name='update_api'),
    url(r'^get/host/', api.get_host, name='get_host'),
    url(r'^get/group/', api.get_group, name='get_group'),
]