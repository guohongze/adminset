#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.views import generic
from .models import Host, HostGroup
from django.http import HttpResponse
from forms import AssetForm
from django.shortcuts import render_to_response, redirect
import csv
import models
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def index(request):
    temp_name = "cmdb/cmdb-header.html"
    host_list = Host.objects.all()
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
    pass


def asset_edit(request):
    pass