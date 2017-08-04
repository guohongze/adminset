#! /usr/bin/env python
# -*- coding: utf-8 -*-
from cmdb.models import Host, HostGroup
from django.shortcuts import render
from subprocess import Popen, PIPE
import sh
from config.views import get_dir
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from lib.log import log
from lib.setup import get_scripts
import logging
scripts_dir = get_dir("s_path")
level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)


@login_required()
@permission_verify()
def index(request):
    temp_name = "setup/setup-header.html"
    all_host = Host.objects.all()
    all_group = HostGroup.objects.all()
    all_scripts = get_scripts(scripts_dir)
    return render(request, 'setup/shell.html', locals())


@login_required()
@permission_verify()
def exec_scripts(request):
    ret = []
    temp_name = "setup/setup-header.html"
    if request.method == 'POST':
        server = request.POST.getlist('mserver', [])
        group = request.POST.getlist('mgroup', [])
        scripts = request.POST.getlist('mscripts', [])
        args = request.POST.getlist('margs')
        command = request.POST.get('mcommand')
        if server:
            if scripts:
                for name in server:
                    host = Host.objects.get(hostname=name)
                    ret.append(host.hostname)
                    logging.info("==========Shell Start==========")
                    logging.info("User:"+request.user.username)
                    logging.info("Host:"+host.hostname)
                    for s in scripts:
                        try:
                            sh.scp(scripts_dir+s, "root@{}:/tmp/".format(host.ip)+s)
                        except:
                            pass
                        cmd = "ssh root@"+host.ip+" "+'"sh /tmp/{} {}"'.format(s, args)
                        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
                        data = p.communicate()
                        ret.append(data)
                        logging.info("Scripts:"+s)
                        for d in data:
                            logging.info(d)
                    logging.info("==========Shell End============")
            else:
                for name in server:
                    host = Host.objects.get(hostname=name)
                    ret.append(host.hostname)
                    logging.info("==========Shell Start==========")
                    logging.info("User:"+request.user.username)
                    logging.info("Host:"+host.hostname)
                    command_list = command.split('\n')
                    for cmd in command_list:
                        cmd = "ssh root@"+host.ip+" "+'"{}"'.format(cmd)
                        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
                        data = p.communicate()
                        ret.append(data)
                        logging.info("command:"+cmd)
                        for d in data:
                            logging.info(d)
                    logging.info("==========Shell End============")
        if group:
            if scripts:
                for g in group:
                    logging.info("==========Shell Start==========")
                    logging.info("User:"+request.user.username)
                    logging.info("Group:"+g)
                    hosts = Host.objects.filter(group__name=g)
                    ret.append(g)
                    for host in hosts:
                        ret.append(host.hostname)
                        for s in scripts:
                            try:
                                sh.scp(scripts_dir+s, "root@{}:/tmp/".format(host.ip)+s)
                            except:
                                pass
                            cmd = "ssh root@"+host.ip+" "+'"sh /tmp/{} {}"'.format(s, args)
                            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
                            data = p.communicate()
                            ret.append(data)
                            logging.info("command:"+cmd)
                            for d in data:
                                logging.info(d)
                    logging.info("==========Shell End============")
            else:
                command_list = []
                command_list = command.split('\n')
                for g in group:
                    logging.info("==========Shell Start==========")
                    logging.info("User:"+request.user.username)
                    logging.info("Group:"+g)
                    hosts = Host.objects.filter(group__name=g)
                    ret.append(g)
                    for host in hosts:
                        ret.append(host.hostname)
                        for cmd in command_list:
                            cmd = "ssh root@"+host.ip+" "+'"{}"'.format(cmd)
                            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
                            data = p.communicate()
                            ret.append(data)
                            logging.info("command:"+cmd)
                            for d in data:
                                logging.info(d)
                    logging.info("==========Shell End============")
        return render(request, 'setup/shell_result.html', locals())
