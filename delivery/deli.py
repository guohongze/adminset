#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from delivery.models import Delivery
from delivery.forms import DeliveryFrom
from accounts.permission import permission_verify
from delivery.tasks import deploy
import os, re
from time import sleep
import json
import time
from cmdb.api import pages


@login_required()
@permission_verify()
def delivery_list(request):
    all_project = []
    if request.user.is_superuser:
        all_project = Delivery.objects.all()
    else:
        projects = request.user.role.delivery.all()
        for p in projects:
            all_project.append(Delivery.objects.get(job_name=p))
    page_len = request.GET.get('page_len', '')
    deploys_list, p, deploys, page_range, current_page, show_first, show_end, end_page = pages(all_project, request)
    return render(request, 'delivery/delivery_list.html', locals())


@login_required
@permission_verify()
def delivery_del(request):
    project_id = request.GET.get('project_id', '')
    if project_id:
        Delivery.objects.filter(id=project_id).delete()

    project_id_all = str(request.POST.get('project_id_all', ''))
    if project_id_all:
        for project_id in project_id_all.split(','):
            Delivery.objects.filter(id=project_id).delete()

    return HttpResponseRedirect(reverse('delivery_list'))


@login_required
@permission_verify()
def delivery_add(request):
    if request.method == 'POST':
        form = DeliveryFrom(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('delivery_list'))
    else:
        form = DeliveryFrom()

    results = {
        'form': form,
        'request': request,
    }
    return render(request, 'delivery/delivery_base.html', results)


@login_required
@permission_verify()
def delivery_edit(request, project_id):
    project = Delivery.objects.get(job_name_id=project_id)
    if request.method == 'POST':
        form = DeliveryFrom(request.POST, instance=project)
        if form.is_valid():
            form.save()
            status = 1
        else:
            status = 2
    else:
        form = DeliveryFrom(instance=project)

    results = {
        'form': form,
        'project_id': project_id,
        'request': request,
    }
    return render(request, 'delivery/delivery_edit.html', locals())


@login_required
@permission_verify()
def delivery_deploy(request, project_id):
    server_list = []
    project = Delivery.objects.get(job_name_id=project_id)
    project.bar_data = 10
    job_name = project.job_name.name
    source_address = project.job_name.source_address
    app_path = project.job_name.appPath
    source_auth = project.source_auth
    if project.auth:
        auth_info = {"username": project.auth.username,
                     "password": project.auth.password,
                     "deploy_port": project.auth.deploy_port,
                     }
    else:
        auth_info = None
    project.status = True
    project.deploy_num += 1
    project.save()
    sleep(2)
    os.system("mkdir -p /var/opt/adminset/workspace/{0}/logs".format(job_name))
    os.system("mkdir -p /var/opt/adminset/workspace/{0}/scripts".format(job_name))
    if app_path == "/":
        return HttpResponse("app deploy destination cannot /")
    # foreign key query need add .all()
    servers = project.serverList.all()
    for server in servers:
        server_ip = str(server.ip)
        server_list.append(server_ip)
    project.bar_data = 15
    rsync_status = project.rsync_delete
    deploy.delay(job_name, server_list, app_path, source_address, project_id, auth_info, rsync_status, source_auth)
    return HttpResponse("ok")


@login_required()
@permission_verify()
def log(request, project_id):
    project = Delivery.objects.get(job_name_id=project_id)
    return render(request, "delivery/results.html", locals())


@login_required()
@permission_verify()
def status(request, project_id):
    project = Delivery.objects.get(job_name_id=project_id)
    bar_data = project.bar_data
    status_val = project.status
    ret = {"bar_data": bar_data, "status": status_val}
    data = json.dumps(ret)
    return HttpResponse(data)


@login_required()
@permission_verify()
def log2(request, project_id):
    ret = []
    project = Delivery.objects.get(job_name_id=project_id)
    job_name = project.job_name.name
    try:
        job_workspace = "/var/opt/adminset/workspace/{0}/".format(job_name)
        log_file = job_workspace + 'logs/deploy-' + str(project.deploy_num) + ".log"
        with open(log_file, 'r+') as f:
            line = f.readlines()
        for l in line:
            a = l + "<br>"
            ret.append(a)
    except IOError:
        ret = "Program is Deploying Please waiting<br>"
    return HttpResponse(ret)


@login_required()
@permission_verify()
def task_stop(request, project_id):
    project = Delivery.objects.get(job_name_id=project_id)
    project.bar_data = 0
    project.status = False
    project.save()
    return HttpResponse("task stop ok")


@login_required()
@permission_verify()
def logs_history(request, project_id):
    project = Delivery.objects.get(job_name_id=project_id)
    job_name = project.job_name.name
    log_path = "/var/opt/adminset/workspace/{0}/logs".format(job_name)
    for logs in os.walk(log_path):
        logs_history = logs[2]
    return render(request, "delivery/logs_history.html", locals())


@login_required()
@permission_verify()
def get_log(request, project_id, logname):
    ret = []
    project = Delivery.objects.get(job_name_id=project_id)
    job_name = project.job_name.name
    log_path = "/var/opt/adminset/workspace/{0}/logs/".format(job_name)
    # log_path = "/var/opt/adminset/workspace/{0}/logs/".format(job_name)
    log_file = log_path + logname
    with open(log_file, 'r+') as f:
        line = f.readlines()
        for l in line:
            l += "<br>"
            ret.append(l)
    return HttpResponse(ret)


@login_required()
@permission_verify()
def log_del(request):
    project_id = request.GET.get('project_id', '')
    logname = request.GET.get('logname', '')
    project = Delivery.objects.get(job_name_id=project_id)
    job_name = project.job_name.name
    log_path = "/var/opt/adminset/workspace/{0}/logs/".format(job_name)
    log_file = log_path + logname
    if project_id and "../" not in logname:
        os.remove(log_file)

    return HttpResponse("ok")


@login_required()
@permission_verify()
def log_delall(request):
    project_id = request.GET.get('project_id', '')
    project = Delivery.objects.get(job_name_id=project_id)
    job_name = project.job_name.name
    log_path = "/var/opt/adminset/workspace/{0}/logs/".format(job_name)
    for l_file in os.walk(log_path):
        for l in l_file[2]:
            del_file = log_path + l
            os.remove(del_file)

    return HttpResponse("ok")