#! /usr/bin/env python
# -*- coding: utf-8 -*-
from cmdb.models import Host
from django.shortcuts import render_to_response, HttpResponse
import os
from subprocess import Popen, PIPE
import sh
scripts_dir = "/etc/ansible/scripts/"


def index(request):
    temp_name = "setup/setup-header.html"
    all_host = Host.objects.all()
    all_scripts = get_scripts(scripts_dir)
    return render_to_response('setup/shell.html', locals())


def exec_scripts(request):
    ret = []
    temp_name = "setup/setup-header.html"
    if request.method == 'POST':
        server = request.POST.getlist('mserver', [])
        scripts = request.POST.getlist('mscripts', [])
        for name in server:
            host = Host.objects.get(hostname=name)
            ret.append(host.hostname)
            for s in scripts:
                sh.scp(scripts_dir+s, "root@{}:/tmp/".format(host.ip)+s)
                cmd = "ssh root@"+host.ip+" "+'"sh /tmp/{}"'.format(s)
                p = Popen(cmd, stdout=PIPE, stderr=PIPE,shell=True)
                data = p.communicate()
                ret.append(data)
        return render_to_response('setup/shell_result.html', locals())


def get_scripts(args):
    files_list = []
    dirs = os.listdir(args)
    for d in dirs:
        if d[0] == '.':
            pass
        elif os.path.isdir(args+d):
            pass
        else:
            files_list.append(d)
    return files_list