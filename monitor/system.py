#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from cmdb.models import Host
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
import json
import time
from api import GetSysData
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
    temp_name = "monitor/monitor-header.html"
    all_host = Host.objects.all()
    return render(request, "monitor/index.html", locals())


@login_required()
@permission_verify()
def host_info(request, hostname, timing):
    temp_name = "monitor/monitor-header.html"
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
    return render(request, "monitor/host_info_{}.html".format(timing), locals())


