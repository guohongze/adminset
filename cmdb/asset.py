#! /usr/bin/env python
# -*- coding: utf-8 -*-

from forms import AssetForm
from django.shortcuts import render_to_response
from models import Host, Idc


def asset_add(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == "POST":
        a_form = AssetForm(request.POST)
        if a_form.is_valid():
            a_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("cmdb/asset_add.html", locals())
    else:
        display_control = "none"
        a_form = AssetForm()
        return render_to_response("cmdb/asset_add.html", locals())


def asset_del(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'POST':
        asset_items = request.POST.getlist('host_check', [])
        if asset_items:
            for n in asset_items:
                Host.objects.filter(id=n).delete()
    host_list = Host.objects.all()
    return render_to_response("cmdb/index.html", locals())


def asset_edit(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'GET':
        hostid = request.GET.get("hostid")
        obj = Host.objects.get(id=hostid)
        allidc = Idc.objects.all()
    return render_to_response("cmdb/asset_edit.html", locals())


def asset_save(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'POST':
        asset_id = request.POST.get('id')
        hostname = request.POST.get('hostname')
        ip = request.POST.get('ip')
        group = request.POST.get('group')
        os = request.POST.get('os')
        vendor = request.POST.get('vendor')
        cpu_model = request.POST.get('cpu_model')
        cpu_num = request.POST.get('cpu_num')
        memory = request.POST.get('memory')
        disk = request.POST.get('disk')
        sn = request.POST.get('sn')
        idc = request.POST.get('idc')
        h_item = Host.objects.get(id=asset_id)
        h_item.hostname = hostname
        h_item.ip = ip
        h_item.group = group
        h_item.os = os
        h_item.vendor = vendor
        h_item.cpu_model = cpu_model
        h_item.cpu_num = cpu_num
        h_item.disk = disk
        h_item.sn = sn
        h_item.idc_id = idc
        h_item.save()
        obj = h_item
        status = 1
    else:
        status = 2
    return render_to_response("cmdb/asset_edit.html",locals())