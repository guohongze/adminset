#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.views import generic
from .models import Host, HostGroup, Idc, ASSET_TYPE, ASSET_STATUS
from django.http import HttpResponse
from forms import AssetForm, IdcForm
from django.shortcuts import render_to_response, redirect
from django.db.models import Q
from cmdb.api import get_object
from cmdb.api import pages
import csv
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
    export = request.GET.get("export", False)
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
            Q(other_ip__contains=keyword) |
            Q(ip__contains=keyword) |
            Q(remote_ip__contains=keyword) |
            Q(comment__contains=keyword) |
            Q(username__contains=keyword) |
            Q(group__name__contains=keyword) |
            Q(cpu__contains=keyword) |
            Q(memory__contains=keyword) |
            Q(disk__contains=keyword) |
            Q(brand__contains=keyword) |
            Q(cabinet__contains=keyword) |
            Q(sn__contains=keyword) |
            Q(system_type__contains=keyword) |
            Q(system_version__contains=keyword))
    assets_list, p, assets, page_range, current_page, show_first, show_end = pages(asset_find, request)
    return render_to_response('cmdb/index.html', locals())


def excel(request):
    host = Host.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cmdb.csv"'
    writer = csv.writer(response)
    writer.writerow(['HostName', 'IP ADDRESS', 'Group', 'Memory', 'Disk', 'CPU', 'Cpu Cores', 'OS', 'IDC'])
    for h in host:
        writer.writerow([h.hostname, h.ip, h.group, h.memory, h.disk, h.cpu_model, h.cpu_num, h.os, str(h.idc).encode('gb2312')])
    return response

    def __unicode__(self):
        return self.name


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