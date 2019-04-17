#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from cmdb import api, idc, asset, group, cabinet


urlpatterns = [
    url(r'^asset/$', asset.asset, name='cmdb'),
    url(r'^assetadd/$', asset.asset_add, name='asset_add'),
    url(r'^assetdel/$', asset.asset_del, name='asset_del'),
    url(r'^assetimport/$', asset.asset_import, name='asset_import'),
    url(r'^assetedit/(?P<ids>\d+)/$', asset.asset_edit, name='asset_edit'),
    url(r'^asset/detail/(?P<ids>\d+)/$', asset.server_detail, name='server_detail'),
    # url(r'^asset/save/$', asset.asset_save, name='asset_save'),
    url(r'^group/$', group.group, name='group'),
    url(r'^groupdel/$', group.group_del, name='group_del'),
    url(r'^groupadd/$', group.group_add, name='group_add'),
    url(r'^groupserverlist/(?P<group_id>\d+)/$', group.server_list, name='group_server_list'),
    url(r'^groupedit/(?P<group_id>\d+)/$', group.group_edit, name='group_edit'),
    # url(r'^group/save/$', group.group_save, name='group_save'),
    url(r'^cabinet/$', cabinet.cabinet, name='cabinet'),
    url(r'^cabinetdel/$', cabinet.cabinet_del, name='cabinet_del'),
    url(r'^cabinetadd/$', cabinet.cabinet_add, name='cabinet_add'),
    url(r'^cabinetserverlist/(?P<cabinet_id>\d+)/$', cabinet.server_list, name='cabinet_server_list'),
    url(r'^cabinetedit/(?P<cabinet_id>\d+)/$', cabinet.cabinet_edit, name='cabinet_edit'),
    url(r'^idc/$', idc.idc, name='idc'),
    url(r'^idcadd/$', idc.idc_add, name='idc_add'),
    url(r'^idcdel/$', idc.idc_del, name='idc_del'),
    url(r'^idcedit/(?P<idc_id>\d+)/$', idc.idc_edit, name='idc_edit'),
    url(r'^idccabinetlist/(?P<idc_id>\d+)/$', idc.cabinet_list, name='idc_cabinet_list'),
    url(r'^collect', api.collect, name='update_api'),
    url(r'^gethost/', api.get_host, name='get_host'),
    url(r'^getgroup/', api.get_group, name='get_group'),
    url(r'^nodestatus/(?P<ids>\d+)/$', asset.node_status, name='node_status'),
]