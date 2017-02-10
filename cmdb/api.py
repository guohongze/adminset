#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Host, HostGroup

try:
    import json
except ImportError,e:
    import simplejson as json


def collect(request):
    req = request
    if req.POST:
        vendor = req.POST.get('vendor')
        group = req.POST.get('group')
        disk = req.POST.get('disk')
        cpu_model = req.POST.get('cpu_model')
        cpu_num = req.POST.get('cpu_num')
        memory = req.POST.get('memory')
        sn = req.POST.get('sn')
        osver = req.POST.get('osver')
        hostname = req.POST.get('hostname')
        ip = req.POST.get('ip')
        try:
            host = Host.objects.get(hostname=hostname)
        except:
            host = Host()
        if req.POST.get('identity'):
            identity = req.POST.get('identity')
            try:
                host = Host.objects.get(identity=identity)
            except:
                host = Host()
        host.hostname = hostname
        host.group = group
        host.cpu_num = int(cpu_num)
        host.cpu_model = cpu_model
        host.memory = int(memory)
        host.sn = sn
        host.disk = disk
        host.os = osver
        host.vendor = vendor
        host.ip = ip
        host.save()
        return HttpResponse("post data successfully!")
    else:
        return HttpResponse("no any post data!")


def get_group(request):
    if request.GET:
        d = []
        try:
            name = request.GET['name']
        except:
            return HttpResponse('you have no data')
        host_groups = HostGroup.objects.get(name=name)
        ret_hg = {'host_group': host_groups.name, 'members': []}
        members = host_groups.members.all()
        for h in members:
            ret_h = {'hostname': h.hostname, 'ipaddr': h.ip}
            ret_hg['members'].append(ret_h)
        d.append(ret_hg)
        return HttpResponse(json.dumps(d))
    else:
        d = []
        host_groups = HostGroup.objects.all()
        for hg in host_groups:
            ret_hg = {'host_group': hg.name, 'members': []}
            members = hg.members.all()
            for h in members:
                ret_h = {'hostname': h.hostname, 'ipaddr': h.ip}
                ret_hg['members'].append(ret_h)
            d.append(ret_hg)
        return HttpResponse(json.dumps(d))


def get_host(request):
    try:
        hostname = request.GET['hostname']
    except:
        return HttpResponse('you have no data')
    try:
        host = Host.objects.get(hostname=hostname)
    except:
        return HttpResponse('no data,please check your hostname')
    data = {'hostname': host.hostname, 'ip': host.ip}
    return HttpResponse(json.dumps({'status': 0, 'message': 'ok', 'data': data}))

