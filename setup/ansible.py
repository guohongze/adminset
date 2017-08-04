#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
from cmdb.models import Host, HostGroup
from django.shortcuts import render
from django.http import HttpResponse
import os
from config.views import get_dir
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
import logging
from lib.log import log
from lib.setup import get_playbook, get_roles

# var info
ansible_dir = get_dir("a_path")
roles_dir = get_dir("r_path")
playbook_dir = get_dir("p_path")
level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)


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
    temp_name = "setup/setup-header.html"
    all_host = Host.objects.all()
    all_dir = get_roles(roles_dir)
    all_pbook = get_playbook(playbook_dir)
    all_group = HostGroup.objects.all()
    return render(request, 'setup/ansible.html', locals())


@login_required()
@permission_verify()
def playbook(request):
    ret = []
    temp_name = "setup/setup-header.html"
    if os.path.exists(ansible_dir + '/gexec.yml'):
        os.remove(ansible_dir + '/gexec.yml')
    else:
        pass
    if request.method == 'POST':
        host = request.POST.getlist('mserver', [])
        group = request.POST.getlist('mgroup', [])
        pbook = request.POST.getlist('splaybook', [])
        roles = request.POST.getlist('mroles', [])
        role_vars = request.POST.get('mvars')

        if host:
            if roles:
                if role_vars:
                    write_role_vars(roles, role_vars)
                for h in host:
                    logging.info("==========ansible tasks start==========")
                    logging.info("User:"+request.user.username)
                    logging.info("host:"+h)
                    with open(ansible_dir + '/gexec.yml', 'w+') as f:
                        flist = ['- hosts: '+h+'\n', '  remote_user: root\n', '  gather_facts: true\n', '  roles:\n']
                        for r in roles:
                            rs = '    - ' + r + '\n'
                            flist.append(rs)
                            logging.info("Role:"+r)
                        f.writelines(flist)
                    cmd = "ansible-playbook"+" " + ansible_dir+'/gexec.yml'
                    p = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
                    data = p.communicate()
                    ret.append(data)
                    for d in data:
                        logging.info(d)
                    logging.info("==========ansible tasks end============")
            else:
                for h in host:
                    for p in pbook:
                        f = open(playbook_dir + p, 'r+')
                        flist = f.readlines()
                        flist[0] = '- hosts: '+h+'\n'
                        f = open(playbook_dir + p, 'w+')
                        f.writelines(flist)
                        f.close()
                        cmd = "ansible-playbook"+" " + playbook_dir + p
                        pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
                        data = pcmd.communicate()
                        ret.append(data)
                        logging.info("==========ansible tasks start==========")
                        logging.info("User:"+request.user.username)
                        logging.info("host:"+h)
                        logging.info("Playbook:"+p)
                        for d in data:
                            logging.info(d)
                        logging.info("==========ansible tasks end============")
            return render(request, 'setup/result.html', locals())

        if group:
            if roles:
                if role_vars:
                    write_role_vars(roles, role_vars)
                for g in group:
                    logging.info("==========ansible tasks start==========")
                    logging.info("User:"+request.user.username)
                    logging.info("group:"+g)
                    f = open(ansible_dir + '/gexec.yml', 'w+')
                    flist = ['- hosts: '+g+'\n', '  remote_user: root\n', '  gather_facts: true\n', '  roles:\n']
                    for r in roles:
                        rs = '    - ' + r + '\n'
                        flist.append(rs)
                        logging.info("Role:"+r)
                    f.writelines(flist)
                    f.close()
                    cmd = "ansible-playbook"+" " + ansible_dir+'/gexec.yml'
                    p = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
                    data = p.communicate()
                    ret.append(data)
                    for d in data:
                        logging.info(d)
                    logging.info("==========ansible tasks end============")
            else:
                for g in group:
                    for p in pbook:
                        f = open(playbook_dir + p, 'r+')
                        flist = f.readlines()
                        flist[0] = '- hosts: '+g+'\n'
                        f = open(playbook_dir + p, 'w+')
                        f.writelines(flist)
                        f.close()
                        cmd = "ansible-playbook"+" " + playbook_dir + p
                        pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
                        data = pcmd.communicate()
                        ret.append(data)
                        logging.info("==========ansible tasks start==========")
                        logging.info("User:"+request.user.username)
                        logging.info("Group:"+g)
                        logging.info("Playbook:"+p)
                        for d in data:
                            logging.info(d)
                        logging.info("==========ansible tasks end============")
            return render(request, 'setup/result.html', locals())


@login_required()
@permission_verify()
def ansible_command(request):
    command_list = []
    ret = []
    count = 1
    temp_name = "setup/setup-header.html"
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
        members = Host.objects.filter(group__name=g)
        for m in members:
            group_item = m.hostname+"\n"
            ansible_file.write(group_item)
    ansible_file.close()
    logging.info("==========ansible tasks start==========")
    logging.info("User:"+request.user.username)
    logging.info("Task: sync cmdb info to ansible hosts")
    logging.info("==========ansible tasks end============")
    return HttpResponse("ok")