#! /usr/bin/env python
# -*- coding: utf-8 -*-

from forms import AssetForm
from django.shortcuts import render_to_response, redirect, HttpResponse, RequestContext
from models import Host, Idc, HostGroup, ASSET_STATUS, ASSET_TYPE
from api import get_object


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
        return render_to_response("cmdb/asset_add.html", locals(), context_instance=RequestContext(request))
    else:
        display_control = "none"
        a_form = AssetForm()
        return render_to_response("cmdb/asset_add.html", locals(), context_instance=RequestContext(request))


# def asset_del(request):
#     temp_name = "cmdb/cmdb-header.html"
#     print request
#     if request.method == 'POST':
#         asset_items = request.POST.getlist('host_check', [])
#         if asset_items:
#             for n in asset_items:
#                 Host.objects.filter(id=n).delete()
#     #host_list = Host.objects.all()
#     return redirect("/cmdb", locals())


def asset_del(request):
    asset_id = request.GET.get('id', '')
    if asset_id:
        Host.objects.filter(id=asset_id).delete()

    if request.method == 'POST':
        asset_batch = request.GET.get('arg', '')
        asset_id_all = str(request.POST.get('asset_id_all', ''))

        if asset_batch:
            for asset_id in asset_id_all.split(','):
                asset = get_object(Host, id=asset_id)
                asset.delete()

    return HttpResponse(u'删除成功')


def asset_edit(request):
    asset_id = request.GET.get('hostid', '')
    asset = get_object(Host, id=asset_id)
    af = AssetForm(instance=asset)
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'GET':
        hostid = request.GET.get("hostid")
        obj = Host.objects.get(id=hostid)
        allidc = Idc.objects.all()
        allgroup = HostGroup.objects.all()
        asset_types = ASSET_TYPE
    return render_to_response("cmdb/asset_edit.html", locals())


def asset_save(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'POST':
        asset_id = request.POST.get('id')
        hostname = request.POST.get('hostname')
        ip = request.POST.get('ip')
        other_ip = request.POST.get('other_ip')
        group = request.POST.get('group')
        asset_type = request.POST.get('asset_type')
        status = request.POST.get('status')
        os = request.POST.get('os')
        vendor = request.POST.get('vendor')
        cpu_model = request.POST.get('cpu_model')
        cpu_num = request.POST.get('cpu_num')
        memory = request.POST.get('memory')
        disk = request.POST.get('disk')
        sn = request.POST.get('sn')
        idc = request.POST.get('idc')
        position = request.POST.get('position')
        memo = request.POST.get('memo')
        h_item = Host.objects.get(id=asset_id)
        h_item.hostname = hostname
        h_item.ip = ip
        h_item.other_ip = other_ip
        h_item.group_id = group
        h_item.asset_type = asset_type
        h_item.status = status
        h_item.os = os
        h_item.vendor = vendor
        h_item.cpu_model = cpu_model
        h_item.cpu_num = cpu_num
        h_item.memory = memory
        h_item.disk = disk
        h_item.sn = sn
        h_item.idc_id = idc
        h_item.position = position
        h_item.memo = memo
        h_item.save()
        obj = h_item
        status = 1
    else:
        status = 2
    return render_to_response("cmdb/asset_edit.html", locals())


def asset_group(request):
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