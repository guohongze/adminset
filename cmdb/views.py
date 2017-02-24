#! /usr/bin/env python
# -*- coding: utf-8 -*-


from django.views import generic
from .models import Host, HostGroup, Idc, ASSET_TYPE, ASSET_STATUS
from django.http import HttpResponse
from forms import AssetForm, IdcForm
from django.shortcuts import render_to_response, redirect
from django.db.models import Q
from cmdb.api import get_object
from cmdb.api import pages, str2gb
import csv, datetime
import models
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def cmdb_index(request):
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
    return render_to_response('cmdb/index.html', locals())


def login(request):
    ret = {}
    if request.method == 'POST':
        user = request.POST.get('username',None)
        pwd = request.POST.get('password',None)
        is_auth = models.UserInfo.objects.filter(username=user,password=pwd).count()
        if is_auth == 1:
            return redirect('/cmdb')
        else:
            ret['status'] = 'user or password error'
            return render_to_response('login2.html', locals())
    else:
        return render_to_response('login2.html', locals())


def hostsync(request):
    group = HostGroup.objects.all()
    ansible_file = open("/etc/ansible/hosts","wb")
    for h in group:
        group_name = "["+h.name+"]"+"\n"
        ansible_file.write(group_name)
        members = h.members.all()
        for m in members:
            #gitlab ansible_host=10.100.1.76 host_name=gitlab
            host_item = m.hostname+" "+"ansible_host="+m.ip+" "+"host_name="+m.hostname+"\n"
            ansible_file.write(host_item)
    ansible_file.close()
    return HttpResponse("ok")
