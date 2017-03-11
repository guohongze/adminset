#! /usr/bin/env python
# -*- coding: utf-8 -*-

from forms import AssetForm
from models import Host, Idc, HostGroup, ASSET_STATUS, ASSET_TYPE
from django.shortcuts import render_to_response, redirect, RequestContext, HttpResponse
from django.db.models import Q
from cmdb.api import get_object
from cmdb.api import pages, str2gb
import csv, datetime
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from django.views.decorators.csrf import csrf_exempt
import sys
reload(sys)
sys.setdefaultencoding('utf8')


@login_required()
@permission_verify()
def asset(request):
    temp_name = "cmdb/cmdb-header.html"
    idc_info = Idc.objects.all()
    host_list = Host.objects.all()
    group_info = HostGroup.objects.all()
    asset_types = ASSET_TYPE
    asset_status = ASSET_STATUS
    idc_name = request.GET.get('idc', '')
    group_name = request.GET.get('group', '')
    asset_type = request.GET.get('asset_type', '')
    status = request.GET.get('status', '')
    keyword = request.GET.get('keyword', '')
    export = request.GET.get("export", '')
    group_id = request.GET.get("group_id", '')
    idc_id = request.GET.get("idc_id", '')
    asset_id_all = request.GET.getlist("id", '')

    if group_id:
        group = get_object(HostGroup, id=group_id)
        if group:
            asset_find = Host.objects.filter(group=group)
    elif idc_id:
        idc = get_object(Idc, id=idc_id)
        if idc:
            asset_find = Host.objects.filter(idc=idc)
    else:
        asset_find = Host.objects.all()

    if idc_name:
        asset_find = asset_find.filter(idc__name__contains=idc_name)

    if group_name:
        asset_find = asset_find.filter(group__name__contains=group_name)

    if asset_type:
        asset_find = asset_find.filter(asset_type__contains=asset_type)

    if status:
        asset_find = asset_find.filter(status__contains=status)

    if keyword:
        asset_find = asset_find.filter(
            Q(hostname__contains=keyword) |
            Q(ip__contains=keyword) |
            Q(other_ip__contains=keyword) |
            Q(os__contains=keyword) |
            Q(vendor__contains=keyword) |
            Q(cpu_model__contains=keyword) |
            Q(cpu_num__contains=keyword) |
            Q(memory__contains=keyword) |
            Q(disk__contains=keyword) |
            Q(sn__contains=keyword) |
            Q(position__contains=keyword) |
            Q(memo__contains=keyword))

    if export == "true":
        if asset_id_all:
            asset_find = []
            for asset_id in asset_id_all:
                asset = get_object(Host, id=asset_id)
                if asset:
                    asset_find.append(asset)
            response = HttpResponse(content_type='text/csv')
            now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
            file_name = 'adminset_cmdb_' + now + '.csv'
            response['Content-Disposition'] = "attachment; filename="+file_name
            writer = csv.writer(response)
            writer.writerow([str2gb('主机名'), str2gb('IP地址'), str2gb('其它IP'), str2gb('主机组'), str2gb('设备类型'), str2gb('设备状态'), str2gb('操作系统'), str2gb('设备厂商'), str2gb('CPU型号'), str2gb('CPU核数'), str2gb('内存大小'), str2gb('硬盘信息'), str2gb('SN号码'), str2gb('所在机房'),str2gb('所在位置'), str2gb('备注信息')])
            for h in asset_find:
                if h.asset_type:
                    at_num = int(h.asset_type)
                    a_type = ASSET_TYPE[at_num-1][1]
                else:
                    a_type = ""
                if h.status:
                    at_as = int(h.status)
                    a_status = ASSET_STATUS[at_as-1][1]
                else:
                    a_status = ""
                writer.writerow([str2gb(h.hostname), h.ip, h.other_ip, str2gb(h.group), str2gb(a_type), str2gb(a_status), str2gb(h.os), str2gb(h.vendor), str2gb(h.cpu_model), str2gb(h.cpu_num), str2gb(h.memory), str2gb(h.disk), str2gb(h.sn), str2gb(h.idc), str2gb(h.position), str2gb(h.memo)])
            return response

    if export == "all":
        host = Host.objects.all()
        response = HttpResponse(content_type='text/csv')
        now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
        file_name = 'adminset_cmdb_' + now + '.csv'
        response['Content-Disposition'] = "attachment; filename=" + file_name
        writer = csv.writer(response)
        writer.writerow([str2gb('主机名'), str2gb('IP地址'), str2gb('其它IP'), str2gb('主机组'), str2gb('设备类型'), str2gb('设备状态'), str2gb('操作系统'), str2gb('设备厂商'), str2gb('CPU型号'), str2gb('CPU核数'), str2gb('内存大小'), str2gb('硬盘信息'), str2gb('SN号码'), str2gb('所在机房'),str2gb('所在位置'), str2gb('备注信息')])
        for h in host:
            if h.asset_type:
                at_num = int(h.asset_type)
                a_type = ASSET_TYPE[at_num-1][1]
            else:
                a_type = ""
            if h.status:
                at_as = int(h.status)
                a_status = ASSET_STATUS[at_as-1][1]
            else:
                a_status = ""
            writer.writerow([str2gb(h.hostname), h.ip, h.other_ip, str2gb(h.group), str2gb(a_type), str2gb(a_status), str2gb(h.os), str2gb(h.vendor), str2gb(h.cpu_model), str2gb(h.cpu_num), str2gb(h.memory), str2gb(h.disk), str2gb(h.sn), str2gb(h.idc), str2gb(h.position), str2gb(h.memo)])
        return response

    assets_list, p, assets, page_range, current_page, show_first, show_end = pages(asset_find, request)
    return render_to_response('cmdb/index.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
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
        return render_to_response("cmdb/asset_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        a_form = AssetForm()
        return render_to_response("cmdb/asset_add.html", locals(), RequestContext(request))


# @csrf_exempt
@login_required()
@permission_verify()
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


@login_required()
@permission_verify()
def asset_edit(request, ids):
    #传参给layui script避免一个status为空的报错
    status = 0
    iasset = get_object(Host, id=ids)
    af = AssetForm(instance=iasset)
    temp_name = "cmdb/cmdb-header.html"
    obj = Host.objects.get(id=ids)
    asset_types = ASSET_TYPE
    return render_to_response("cmdb/asset_edit.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
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
        #传参给lyaui以触发回调
        status = 1
    else:
        status = 2
    return render_to_response("cmdb/asset_edit.html", locals(), RequestContext(request))


# @login_required()
# @permission_verify()
# def asset_group(request):
#     temp_name = "cmdb/cmdb-header.html"
#     group_info = HostGroup.objects.all()
#     return render_to_response('cmdb/group.html', locals())