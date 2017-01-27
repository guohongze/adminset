#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.authtoken import views


urlpatterns = [
    url(r'^$', views.obtain_auth_token),
]