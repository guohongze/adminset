#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from navi import views

urlpatterns = [
    url(r'^navilist/$', views.index, name='navi'),
    url(r'^naviadd/$', views.add, name='naviadd'),
    url(r'^navimanage/$', views.manage, name='navimanage'),
    url(r'^navidelete/$', views.delete, name='navidelete'),
    url(r'^naviedit/$', views.edit, name='naviedit'),
    url(r'^navisave/$', views.save, name='navisave'),
]