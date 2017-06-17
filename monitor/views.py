from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response, redirect, RequestContext, HttpResponse
from cmdb.models import Host
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from pymongo import MongoClient
import json


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
    data_percent = []
    client = MongoClient("127.0.0.1", 27017)
    db = client.sys_info
    collection = db[hostname]
    cursor = collection.find()
    for doc in cursor:
        unix_time = doc['timestamp']
        cpu_percent = doc['cpu']['percent']
        data_percent.append(cpu_percent)
        data_time.append(unix_time)
    data = {"data_time": data_time, "data_percent": data_percent}
    return HttpResponse(json.dumps(data))
