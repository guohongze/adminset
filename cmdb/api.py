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
        product = req.POST.get('product')
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
        identity = req.POST.get('identity')
        try:
            host = Host.objects.get(identity=identity)
        except:
            host = Host()
        host.hostname = hostname
        host.product = product
        host.cpu_num = int(cpu_num)
        host.cpu_model = cpu_model
        host.memory = int(memory)
        host.sn = sn
        host.os = osver
        host.vendor = vendor
        host.ip = ip
        host.save()
        return HttpResponse("post data successfully!")
    else:
        return HttpResponse("no any post data!")

"""
def gethostsjson(req):
    if req.GET:
        d = []
        hostgroups = HostGroup.objects.all()
        for hg in hostgroups:
            ret_hg = {'hostgroup': hg.name, 'members': []}
            members = hg.members.all()
            for h in members:
                ret_h = {'hostname': h.hostname, 'ipaddr':[i.ipaddr for i in h.ipaddr_set.all()]}
                ret_hg['members'].append(ret_h)
            d.append(ret_hg)
        ret = {'status': 1, 'data': d, 'message': 'OK'}
        return HttpResponse(json.dumps(ret))
    else:
        return HttpResponse('Nothing of hosts to json.dumps!')
"""


def getj(request):
    d = []
    hostgroups = HostGroup.objects.all()
    for hg in hostgroups:
        ret_hg = {'hostgroup': hg.name, 'members': []}
        members = hg.members.all()
        for h in members:
            #ret_h = {'hostname': h.hostname, 'ipaddr':[i.ipaddr for i in h.ipaddr_set.all()]}
            ips = [i.ipaddr for i in h.ipaddr_set.all()]
            if ips:
                ret_h = {'hostname': h.hostname, 'ipaddr': ips[0]}
                ret_hg['members'].append(ret_h)
        d.append(ret_hg)
    ret = {'status': 1, 'data': d, 'message': 'OK'}
    return HttpResponse(json.dumps(ret))


def gett(request):
    d=""
    hostgroups = HostGroup.objects.all()
    for hg in hostgroups:
        members = hg.members.all()
        for h in members:
            ips = ','.join([i.ipaddr for i in h.ipaddr_set.all()])
            d += "%s %s %s\n" % (hg.name, h.hostname, ips)
    return HttpResponse(d)


def geti(request):
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

