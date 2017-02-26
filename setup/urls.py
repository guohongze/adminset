#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views, ansible, shell


urlpatterns = [
    url(r'^$', ansible.index, name='ansible'),
    url(r'^shell', shell.index, name='shell'),
    url(r'^exec_scripts', shell.exec_scripts, name='exec_scripts'),
    url(r'^playbook', ansible.playbook, name='playbook'),
    url(r'^acommand', ansible.ansible_command, name='acommand'),
    url(r'^host_sync', ansible.host_sync, name='host_sync'),
]