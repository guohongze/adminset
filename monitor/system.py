#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from cmdb.models import Host, Idc, HostGroup
from appconf.product import Product
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
import json
import time
from monitor.api import GetSysData
from django.views.decorators.csrf import csrf_exempt
from delivery.models import Delivery

TIME_SECTOR = (
            3600,
            3600*3,
            3600*5,
            86400,
            86400*3,
            86400*7,
)


@login_required()
@permission_verify()
def get_cpu(request, hostname, timing):
    data_time = []
    cpu_percent = []
    range_time = TIME_SECTOR[int(timing)]
    cpu_data = GetSysData(hostname, "cpu", range_time)
    for doc in cpu_data.get_data():
        unix_time = doc['timestamp']
        times = time.localtime(unix_time)
        dt = time.strftime("%m%d-%H:%M", times)
        data_time.append(dt)
        c_percent = doc['cpu']['percent']
        cpu_percent.append(c_percent)
    data = {"data_time": data_time, "cpu_percent": cpu_percent}
    return HttpResponse(json.dumps(data))


@login_required()
@permission_verify()
def get_mem(request, hostname, timing):
    data_time = []
    mem_percent = []
    range_time = TIME_SECTOR[int(timing)]
    mem_data = GetSysData(hostname, "mem", range_time)
    for doc in mem_data.get_data():
        unix_time = doc['timestamp']
        times = time.localtime(unix_time)
        dt = time.strftime("%m%d-%H:%M", times)
        data_time.append(dt)
        m_percent = doc['mem']['percent']
        mem_percent.append(m_percent)
    data = {"data_time": data_time, "mem_percent": mem_percent}
    return HttpResponse(json.dumps(data))


@login_required()
@permission_verify()
def get_disk(request, hostname, timing, partition):
    data_time = []
    disk_percent = []
    disk_name = ""
    range_time = TIME_SECTOR[int(timing)]
    disk = GetSysData(hostname, "disk", range_time)
    for doc in disk.get_data():
        unix_time = doc['timestamp']
        times = time.localtime(unix_time)
        dt = time.strftime("%m%d-%H:%M", times)
        data_time.append(dt)
        d_percent = doc['disk'][int(partition)]['percent']
        disk_percent.append(d_percent)
        if not disk_name:
            disk_name = doc['disk'][int(partition)]['mountpoint']
    data = {"data_time": data_time, "disk_name": disk_name, "disk_percent": disk_percent}
    return HttpResponse(json.dumps(data))


@login_required()
@permission_verify()
def get_net(request, hostname, timing, net_id):
    data_time = []
    nic_in = []
    nic_out = []
    nic_name = ""
    range_time = TIME_SECTOR[int(timing)]
    net = GetSysData(hostname, "net", range_time)
    for doc in net.get_data():
        unix_time = doc['timestamp']
        times = time.localtime(unix_time)
        dt = time.strftime("%m%d-%H:%M", times)
        data_time.append(dt)
        in_ = doc['net'][int(net_id)]['traffic_in']
        out_ = doc['net'][int(net_id)]['traffic_out']
        nic_in.append(in_)
        nic_out.append(out_)
        if not nic_name:
            nic_name = doc['net'][int(net_id)]['nic_name']
    data = {"data_time": data_time, "nic_name": nic_name, "traffic_in": nic_in, "traffic_out": nic_out}
    return HttpResponse(json.dumps(data))


@login_required()
@permission_verify()
def index(request):
    all_host = Host.objects.all()
    idcs = Idc.objects.all()
    return render(request, "monitor/index.html", locals())


@login_required()
@permission_verify()
def host_info(request, hostname, timing):
    # 传递磁盘号给前端JS,用以迭代分区图表
    disk = GetSysData(hostname, "disk", 3600, 1)
    disk_data = disk.get_data()
    partitions_len = []
    for d in disk_data:
        p = len(d["disk"])
        for x in range(p):
            partitions_len.append(x)
    # 传递网卡号给前端,用以迭代分区图表
    net = GetSysData(hostname, "net", 3600, 1)
    nic_data = net.get_data()
    nic_len = []
    for n in nic_data:
        p = len(n["net"])
        for x in range(p):
            nic_len.append(x)
    return render(request, "monitor/host_info.html", locals())


def host_tree():
    host_node = []
    for idc in Idc.objects.all():
        single_server_list = []
        for host in idc.host_set.all():
            if not host.cabinet_set.all():
                single_server_list.append({'name': host.hostname, 'url': "/monitor/system/{}/0/".format(host.hostname), 'target':"myframe"})
        cabinet_list = []
        cabinets = idc.cabinet_set.all()
        for cabinet in cabinets:
            server_list = []
            servers = cabinet.serverList.all()
            for server in servers:
                server_data = {'name': server.hostname, 'url': "/monitor/system/{}/0/".format(server.hostname), 'target':"myframe"}
                server_list.append(server_data)
            cabinet_data = {'name': cabinet.name, 'children': server_list}
            cabinet_list.append(cabinet_data)
            del server_list
        data = {"name": idc.name, "open": False, "children": cabinet_list + single_server_list }
        del cabinet_list
        host_node.append(data)
    return host_node


def group_tree():
    group_node = []
    for group in HostGroup.objects.all():
        server_list = []
        servers = group.serverList.all()
        for server in servers:
            server_data = {'name': server.hostname, 'url': "/monitor/system/{}/0/".format(server.hostname), 'target':"myframe"}
            server_list.append(server_data)
        group_data = {'name': group.name, "open": False, 'children': server_list}
        group_node.append(group_data)
        del server_list
    return group_node


# def product_tree():
#     product_node = []
#     for pdt in Product.objects.all():
#         project_list = []
#         projects = pdt.project_set.all()
#         for pjs in projects:
#             server_list = []
#             p2 = Delivery.objects.get(job_name_id=pjs.id)
#             servers = p2.serverList.all()
#             for server in servers:
#                 server_data = {'name': server.hostname, 'url': "/monitor/system/{}/0/".format(server.hostname), 'target':"myframe"}
#                 server_list.append(server_data)
#             project_data = {'name': pjs.name, 'children': server_list}
#             project_list.append(project_data)
#             del server_list
#         data = {"name": pdt.name, "open": False, "children": project_list}
#         del project_list
#         product_node.append(data)
#     return product_node


@login_required
@csrf_exempt
def tree_node(request):
    all_node = host_tree() + group_tree() #+ product_tree()
    return HttpResponse(json.dumps(all_node))
