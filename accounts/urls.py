#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from accounts import user


urlpatterns = [
    # url(r'^$', user.user_list, name='accounts'),
    url(r'^login/$', user.login, name='login'),
    url(r'^logout/$', user.logout, name='logout'),
    url(r'^user/list/$', user.user_list, name='user_list'),
    url(r'^user/add/$', user.user_add, name='user_add'),
    url(r'^user/delete/(?P<ids>\d+)/$', user.user_del, name='user_del'),
    url(r'^user/edit/(?P<ids>\d+)/$', user.user_edit, name='user_edit'),
    url(r'^reset/password/(?P<ids>\d+)/$', user.reset_pwd, name='reset_pwd'),
    url(r'^change/password/$', user.change_password, name='change_password'),
]