#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path
from navi import views

urlpatterns = [
    path('navilist/', views.index, name='navi'),
    path('naviadd/', views.add, name='naviadd'),
    path('navimanage/', views.manage, name='navimanage'),
    path('navidelete/', views.delete, name='navidelete'),
    path('naviedit/', views.edit, name='naviedit'),
    path('navisave/', views.save, name='navisave'),
] 