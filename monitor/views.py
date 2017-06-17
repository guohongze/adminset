from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response, redirect, RequestContext, HttpResponse
from cmdb.models import Host
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from pymongo import MongoClient
import json, time


@login_required()
@permission_verify()
def index(request):
    temp_name = "monitor/monitor-header.html"
    all_host = Host.objects.all()
    return render_to_response("monitor/index.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def host_info(request, hostname):
    temp_name = "monitor/monitor-header.html"
    return render_to_response("monitor/host_info.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def get_sys_data(request, hostname):
    data_time = []
    cpu_percent = []
    memory_percent = []
    client = MongoClient("127.0.0.1", 27017)
    db = client.sys_info
    collection = db[hostname]
    cursor = collection.find()
    now = int(time.time())
    for doc in cursor:
        unix_time = doc['timestamp']
        if unix_time >= now-3600:
            times = time.localtime(unix_time)
            dt = time.strftime("%m%d-%H:%M:%S", times)
            # get cpu data
            c_percent = doc['cpu']['percent']
            cpu_percent.append(c_percent)
            data_time.append(dt)
            # get mem data
            m_percent = doc['mem']['percent']
            memory_percent.append(m_percent)
    data = {"data_time": data_time, "cpu_percent": cpu_percent, "memory_percent": memory_percent}
    return HttpResponse(json.dumps(data))
