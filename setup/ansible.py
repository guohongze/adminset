#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
from cmdb.models import Host, HostGroup
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os, json
from config.views import get_dir
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
import logging
from lib.log import log
from lib.setup import get_playbook, get_roles
from setup.tasks import task_exec
from lib.common import GetRedis
# var info
ansible_dir = get_dir("a_path")
roles_dir = get_dir("r_path")
playbook_dir = get_dir("p_path")
level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)

redis_host = get_dir("redis_host")
redis_password = get_dir("redis_password")
redis_port = get_dir("redis_port")
redis_db = get_dir("redis_db")

def write_role_vars(roles, vargs):

    r_vars = vargs.split('\r\n')
    for r in roles:

        if vargs:
            if os.path.exists(roles_dir+r+"/vars"):
                pass
            else:
                os.mkdir(roles_dir+r+"/vars")

            with open(roles_dir+r+'/vars/main.yml', 'wb+') as role_file:
                role_file.writelines("---\n")
                for x in r_vars:
                    rs = x + '\n'
                    role_file.writelines(rs)
    return True


@login_required()
@permission_verify()
def index(request):
    all_host = Host.objects.all()
    all_dir = get_roles(roles_dir)
    all_pbook = get_playbook(playbook_dir)
    all_group = HostGroup.objects.all()
    return render(request, 'setup/ansible.html', locals())


@login_required()
@permission_verify()
def playbook(request):
    ret = []
    if os.path.exists(ansible_dir + '/gexec.yml'):
        os.remove(ansible_dir + '/gexec.yml')
    if os.path.exists(log_path + '/ansible.log'):
        os.remove(log_path + '/ansible.log')
    else:
        pass
    if request.method == 'POST':
        host = request.POST.getlist('mserver', [])
        group = request.POST.getlist('mgroup', [])
        pbook = request.POST.getlist('splaybook', [])
        roles = request.POST.getlist('mroles', [])
        role_vars = request.POST.get('mvars')
        r = GetRedis()
        res = r.connect()
        res.set("ansible_status", 1)
        task_exec(request, host, group, pbook, roles, role_vars, write_role_vars)

    return HttpResponse("ok")

@login_required()
def execlog(request):
    ret = []
    try:
        log_file = "/var/opt/adminset/logs/ansible.log"
        with open(log_file, 'r+') as f:
            line = f.readlines()
        for l in line:
            a = l + "<br>"
            ret.append(a)
    except IOError:
        ret = "Ansible is running please waiting<br>"
    return HttpResponse(ret)

@login_required()
def execlog2(request):
    return render(request, 'setup/results.html')

@login_required()
def exec_status(request, exec_type):
    r = GetRedis()
    res = r.connect()
    if exec_type == "1":
        data = res.get("ansible_status")
    elif exec_type == "2":
        data = res.get("shell_status")
    else:
        data = False
    return HttpResponse(data)

@login_required()
@permission_verify()
def ansible_command(request):
    command_list = []
    ret = []
    count = 1
    if request.method == 'POST':
        mcommand = request.POST.get('mcommand')
        command_list = mcommand.split('\n')
        for command in command_list:
            if command.startswith("ansible"):
                p = Popen(command, stdout=PIPE, stderr=PIPE,shell=True)
                data = p.communicate()
                ret.append(data)
            else:
                data = "your command " + str(count) + "  is invalid!"
                ret.append(data)
            count += 1
            logging.info("==========ansible tasks start==========")
            logging.info("User:"+request.user.username)
            logging.info("command:"+command)
            for d in data:
                logging.info(d)
            logging.info("==========ansible tasks end============")
        return render(request, 'setup/result.html', locals())


@login_required()
@permission_verify()
def host_sync(request):
    group = HostGroup.objects.all()
    ansible_file = open(ansible_dir+"/hosts", "wb")
    all_host = Host.objects.all()
    for host in all_host:
        #gitlab ansible_host=10.100.1.76 host_name=gitlab
        host_item = host.hostname+" "+"ansible_host="+host.ip+" "+"host_name="+host.hostname+"\n"
        ansible_file.write(host_item)
    for g in group:
        group_name = "["+g.name+"]"+"\n"
        ansible_file.write(group_name)
        get_member = HostGroup.objects.get(name=g)
        members = get_member.serverList.all()
        for m in members:
            group_item = m.hostname+"\n"
            ansible_file.write(group_item)
    ansible_file.close()
    logging.info("==========ansible tasks start==========")
    logging.info("User:"+request.user.username)
    logging.info("Task: sync cmdb info to ansible hosts")
    logging.info("==========ansible tasks end============")
    return HttpResponse("ok")


@login_required()
@permission_verify()
def ansible_log(request, project_id):
    ret = []
    try:
        log_file = "/var/opt/adminset/logs/ansible.log"
        with open(log_file, 'r+') as f:
            line = f.readlines()
        for l in line:
            a = l + "<br>"
            ret.append(a)
    except IOError:
        ret = "ansible is executing Please waiting<br>"
    return HttpResponse(ret)