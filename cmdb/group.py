#! /usr/bin/env python
# -*- coding: utf-8 -*-

from forms import AssetForm
from django.shortcuts import render_to_response
from models import Host, Idc, HostGroup


def group(request):
    temp_name = "cmdb/cmdb-header.html"
    group_info = HostGroup.objects.all()
    return render_to_response('cmdb/group.html', locals())


def group_del(request):
    pass


def group_add(request):
    pass


def group_edit(request):
    pass


def group_save(request):
    pass