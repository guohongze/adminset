#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.views import generic
from .models import Host, HostGroup
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
import csv
import models
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def cmdb(request):
    host_list = Host.objects.all()
    return render_to_response('cmdb.html', locals())


def index3(request):
    host_list = Host.objects.all()
    return render_to_response('index.html',locals())

def ansible(request):
    host_list = Host.objects.all()
    hostgroup = HostGroup.objects.all()
    return render_to_response('ansible.html',locals())

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'host_list'

    def get_queryset(self):
        return Host.objects.order_by('hostname')


def excel(request):
    host = Host.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cmdb.csv"'
    writer = csv.writer(response)
    writer.writerow(['HostName', 'IP ADDRESS', 'Group', 'Memory', 'Disk', 'CPU', 'Cpu Cores', 'OS', 'IDC'])
    for h in host:
        writer.writerow([h.hostname, h.ip, h.group, h.memory, h.disk, h.cpu_model, h.cpu_num, h.os, str(h.idc).encode('gb2312')])
    return response

    def __str__(self):
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
            return render_to_response('cmdb/login.html', locals())
    else:
        return render_to_response('cmdb/login.html', locals())