#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from branches import region, branch, resource

urlpatterns = [
    url(r'^$', region.region_list, name='branches'),
    url(r'^regionadd/$', region.region_add, name='region_add'),
    url(r'^region/$', region.region_list, name='region_list'),
    url(r'^regionbranchinfo/(?P<region_id>\d+)/$', region.branch_detail, name='branch_detail'),
    url(r'^regionedit/(?P<region_id>\d+)/$', region.region_edit, name='region_edit'),
    url(r'^regiondel/$', region.region_del, name='region_del'),
    url(r'^branchadd/$', branch.branch_add, name='branch_add'),
    url(r'^branch/$', branch.branch_list, name='branch_list'),
    url(r'^branchedit/(?P<branch_id>\d+)/$', branch.branch_edit, name='branch_edit'),
    url(r'^branchdel/$', branch.branch_del, name='branch_del'),
    url(r'^branchexport/$', branch.branch_export, name='branch_export'),
    url(r'^branchresourceinfo/(?P<branch_id>\d+)/$', branch.resource_detail, name='resource_detail'),
    url(r'^resourceadd/$', resource.resource_add, name='resource_add'),
    url(r'^resource/$', resource.resource_list, name='resource_list'),
    url(r'^resourceedit/(?P<resource_id>\d+)/$', resource.resource_edit, name='resource_edit'),
    url(r'^resourcedel/$', resource.resource_del, name='resource_del'),
    url(r'^resourceexport/$', resource.resource_export, name='resource_export'),
]