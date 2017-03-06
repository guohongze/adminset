#! /usr/bin/env python
# -*- coding: utf-8 -*-
from cmdb.models import Host, HostGroup
from django.shortcuts import render_to_response, HttpResponse
import os
from subprocess import Popen, PIPE
import sh
from config.views import get_dir
scripts_dir = get_dir("s_path")


def index(request):
    temp_name = "setup/setup-header.html"
    all_host = Host.objects.all()
    all_group = HostGroup.objects.all()
    all_scripts = get_scripts(scripts_dir)
    return render_to_response('setup/shell.html', locals())


def exec_scripts(request):
    ret = []
    temp_name = "setup/setup-header.html"
    if request.method == 'POST':
        server = request.POST.getlist('mserver', [])
        group = request.POST.getlist('mgroup', [])
        scripts = request.POST.getlist('mscripts', [])
        command = request.POST.get('mcommand')
        if server:
            if scripts:
                for name in server:
                    host = Host.objects.get(hostname=name)
                    ret.append(host.hostname)
                    for s in scripts:
                        sh.scp(scripts_dir+s, "root@{}:/tmp/".format(host.ip)+s)
                        cmd = "ssh root@"+host.ip+" "+'"sh /tmp/{}"'.format(s)
                        p = Popen(cmd, stdout=PIPE, stderr=PIPE,shell=True)
                        data = p.communicate()
                        ret.append(data)
            else:
                for name in server:
                    host = Host.objects.get(hostname=name)
                    ret.append(host.hostname)
                    command_list = command.split('\n')
                    for cmd in command_list:
                        cmd = "ssh root@"+host.ip+" "+'"{}"'.format(cmd)
                        p = Popen(cmd, stdout=PIPE, stderr=PIPE,shell=True)
                        data = p.communicate()
                        ret.append(data)
        if group:
            if scripts:
                for g in group:
                    hosts = Host.objects.filter(group__name=g)
                    ret.append(g)
                    for host in hosts:
                        ret.append(host.hostname)
                        for s in scripts:
                            sh.scp(scripts_dir+s, "root@{}:/tmp/".format(host.ip)+s)
                            cmd = "ssh root@"+host.ip+" "+'"sh /tmp/{}"'.format(s)
                            p = Popen(cmd, stdout=PIPE, stderr=PIPE,shell=True)
                            data = p.communicate()
                            ret.append(data)
            else:
                command_list = []
                command_list = command.split('\n')
                for g in group:
                    hosts = Host.objects.filter(group__name=g)
                    ret.append(g)
                    for host in hosts:
                        ret.append(host.hostname)
                        for cmd in command_list:
                            cmd = "ssh root@"+host.ip+" "+'"{}"'.format(cmd)
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
