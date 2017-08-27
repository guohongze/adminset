#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
import appowner
import product
import project

urlpatterns = [
    url(r'^$', product.product_list, name='appconf'),
    url(r'^appowner/add/$', appowner.appowner_add, name='appowner_add'),
    url(r'^appowner/add/mini/$', appowner.appowner_add_mini, name='appowner_add_mini'),
    url(r'^appowner/list/$', appowner.appowner_list, name='appowner_list'),
    url(r'^appowner/edit/(?P<appowner_id>\d+)/$', appowner.appowner_edit, name='appowner_edit'),
    url(r'^appowner/delete/$', appowner.appowner_del, name='appowner_del'),
    url(r'^product/add/$', product.product_add, name='product_add'),
    url(r'^product/list/$', product.product_list, name='product_list'),
    url(r'^product/project_list/(?P<product_id>\d+)/$', product.project_list, name='product_project_list'),
    url(r'^product/edit/(?P<product_id>\d+)/$', product.product_edit, name='product_edit'),
    url(r'^product/delete/$', product.product_del, name='product_del'),
    url(r'^project/add/$', project.project_add, name='project_add'),
    url(r'^project/list/$', project.project_list, name='project_list'),
    url(r'^project/edit/(?P<project_id>\d+)/$', project.project_edit, name='project_edit'),
    url(r'^project/delete/$', project.project_del, name='project_del'),
    url(r'^project/export/$', project.project_export, name='project_export'),
]