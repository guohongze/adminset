#! /usr/bin/env python
# -*- coding: utf-8 -*-
from cmdb.models import Host, HostGroup
from django.shortcuts import render, HttpResponse
from config.views import get_dir
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from lib.log import log
from lib.setup import get_scripts
from lib.common import GetRedis
from setup.tasks import shell_task
import os
scripts_dir = get_dir("s_path")
level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)


@login_required()
@permission_verify()
def index(request):
    all_host = Host.objects.all()
    all_group = HostGroup.objects.all()
    all_scripts = get_scripts(scripts_dir)
    return render(request, 'setup/shell.html', locals())


@login_required()
@permission_verify()
def exec_scripts(request):
    if os.path.exists(log_path + "/execlog/shell_{0}.log".format(request.user.username)):
        os.remove(log_path + "/execlog/shell_{0}.log".format(request.user.username))
    if request.method == 'POST':
        server = request.POST.getlist('mserver', [])
        group = request.POST.getlist('mgroup', [])
        scripts = request.POST.getlist('mscripts', [])
        args = request.POST.getlist('margs')
        shell_command = request.POST.get('mcommand')

        #connect redis for record shell running status
        res = GetRedis.connect()
        res.set("shell_{0}".format(request.user.username), 1)
        # run async shell tasks
        shell_task(request, server, group, scripts, args, shell_command)

        return HttpResponse("ok")

@login_required()
def shellinfo(request):
    ret = []
    try:
        log_file = "/var/opt/adminset/logs/execlog/shell_{0}.log".format(request.user.username)
        with open(log_file, 'r+') as f:
            line = f.readlines()
        for l in line:
            a = l + "<br>"
            ret.append(a)
    except IOError:
        ret = "Log file is empty waiting for created<br>"
    return HttpResponse(ret)

@login_required()
def logpage(request):
    return render(request, 'setup/shell_result.html')