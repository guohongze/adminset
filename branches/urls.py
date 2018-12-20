#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from branches import region, branch, resource

urlpatterns = [
    url(r'^$', region.region_list, name='branches'),
    url(r'^region/add/$', region.region_add, name='region_add'),
    url(r'^region/list/$', region.region_list, name='region_list'),
    url(r'^region/branch_detail/(?P<region_id>\d+)/$', region.branch_detail, name='branch_detail'),
    url(r'^region/edit/(?P<region_id>\d+)/$', region.region_edit, name='region_edit'),
    url(r'^region/delete/$', region.region_del, name='region_del'),
    url(r'^branch/add/$', branch.branch_add, name='branch_add'),
    url(r'^branch/list/$', branch.branch_list, name='branch_list'),
    url(r'^branch/edit/(?P<branch_id>\d+)/$', branch.branch_edit, name='branch_edit'),
    url(r'^branch/delete/$', branch.branch_del, name='branch_del'),
    url(r'^branch/export/$', branch.branch_export, name='branch_export'),
    url(r'^branch/resource_detail/(?P<branch_id>\d+)/$', branch.resource_detail, name='resource_detail'),
    url(r'^resource/add/$', resource.resource_add, name='resource_add'),
    url(r'^resource/list/$', resource.resource_list, name='resource_list'),
    url(r'^resource/edit/(?P<resource_id>\d+)/$', resource.resource_edit, name='resource_edit'),
    url(r'^resource/delete/$', resource.resource_del, name='resource_del'),
    url(r'^resource/export/$', resource.resource_export, name='resource_export'),
]