#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.ansible, name='ansible'),
    url(r'^shell', views.shell, name='shell'),
    url(r'^playbook', views.playbook, name='playbook'),
    url(r'^ansible_command', views.ansible_command, name='ansible_command'),
    url(r'^host_sync', views.host_sync, name='host_sync'),
]