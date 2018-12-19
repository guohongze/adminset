#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from branches import branch

urlpatterns = [
    url(r'^$', branch.branch_list, name='branches'),
    url(r'^branch/add/$', branch.branch_add, name='branch_add'),
    url(r'^branch/list/$', branch.branch_list, name='branch_list'),
    # url(r'^product/project_list/(?P<product_id>\d+)/$', product.project_list, name='product_project_list'),
    url(r'^branch/edit/(?P<branch_id>\d+)/$', branch.branch_edit, name='branch_edit'),
    url(r'^branch/delete/$', branch.branch_del, name='branch_del'),
    # url(r'^project/add/$', project.project_add, name='project_add'),
    # url(r'^project/list/$', project.project_list, name='project_list'),
    # url(r'^project/edit/(?P<project_id>\d+)/$', project.project_edit, name='project_edit'),
    # url(r'^project/delete/$', project.project_del, name='project_del'),
    # url(r'^project/export/$', project.project_export, name='project_export'),
]