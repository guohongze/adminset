#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from zabbix import views
from jsonrpc.views import browse
from jsonrpc import jsonrpc_site

urlpatterns = [
    # # django jsonrpc
    url(r'^json/browse/', browse, name="jsonrpc_browser"),
    # for the graphical browser/web console only, omissible
    url(r'^json/', jsonrpc_site.dispatch, name="jsonrpc_mountpoint"),
    url(r'^json/(?P<method>[a-zA-Z0-9.]+)$', jsonrpc_site.dispatch),  # for HTTP GET only, also omissible
    url(r'^listapi', views.listapi),
    url(r'^zabbixapi', views.zabbixapi),
    url(r'^zabbix_template', views.zabbix_template),
    url(r'^getapi', views.getapi),
    url(r'^test', views.test),
    # url(r'^template', views.template)
]
