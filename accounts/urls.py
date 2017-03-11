#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from accounts import user, role, permission


urlpatterns = [
    # url(r'^$', user.user_list, name='accounts'),
    url(r'^login/$', user.login, name='login'),
    url(r'^logout/$', user.logout, name='logout'),
    url(r'^user/list/$', user.user_list, name='user_list'),
    url(r'^user/add/$', user.user_add, name='user_add'),
    url(r'^user/delete/(?P<ids>\d+)/$', user.user_del, name='user_del'),
    url(r'^user/edit/(?P<ids>\d+)/$', user.user_edit, name='user_edit'),
    url(r'^reset/password/(?P<ids>\d+)/$', user.reset_password, name='reset_password'),
    url(r'^change/password/$', user.change_password, name='change_password'),
    url(r'^role/add/$', role.role_add, name='role_add'),
    url(r'^role/list/$', role.role_list, name='role_list'),
    url(r'^role/edit/(?P<ids>\d+)/$', role.role_edit, name='role_edit'),
    url(r'^role/delete/(?P<ids>\d+)/$', role.role_del, name='role_del'),
    url(r'^permission/deny/$', permission.permission_deny, name='permission_deny'),
    url(r'^permission/add/$', permission.permission_add, name='permission_add'),
    url(r'^permission/list/$', permission.permission_list, name='permission_list'),
    url(r'^permission/edit/(?P<ids>\d+)/$', permission.permission_edit, name='permission_edit'),
    url(r'^permission/delete/(?P<ids>\d+)/$', permission.permission_del, name='permission_del'),
]