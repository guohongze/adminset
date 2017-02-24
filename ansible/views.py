#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT
from cmdb.models import Host, HostGroup
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
import os

ansible_dir = "/etc/ansible"


def ansible(request):
    temp_name = "ansible/ansible-header.html"
    all_host = Host.objects.all()
    roles_dir = ansible_dir+"/roles/"
    pbook_dir = ansible_dir+"/pbook/"
    all_dir = get_roles(roles_dir)
    all_pbook = get_pbook(pbook_dir)
    all_group = HostGroup.objects.all()
    return render_to_response('ansible/index.html', locals())


def get_roles(args):
    dir_list = []
    dirs = os.listdir(args)
    for d in dirs:
        if d[0] == '.':
            pass
        elif os.path.isfile(args+d):
            pass
        else:
            dir_list.append(d)
    return dir_list


def get_pbook(args):
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


def playbook(request):
    ret = []
    temp_name = "ansible/ansible-header.html"
    if os.path.exists(ansible_dir + '/gexec.yml'):
        os.remove(ansible_dir + '/gexec.yml')
    else:
        pass
    if request.method == 'POST':
        host = request.POST.getlist('mserver', [])
        group = request.POST.getlist('mgroup', [])
        pbook = request.POST.getlist('splaybook', [])
        roles = request.POST.getlist('mplaybook', [])
    if host:
        if roles:
            for h in host:
                f = open(ansible_dir + '/gexec.yml', 'w+')
                flist = ['- hosts: '+h+'\n', '  remote_user: root\n', '  gather_facts: false\n', '  roles:\n']
                for r in roles:
                    rs = '    - ' + r + '\n'
                    flist.append(rs)
                f.writelines(flist)
                f.close()
                cmd = "ansible-playbook"+" " + ansible_dir+'/gexec.yml'
                p = Popen(cmd, stderr=STDOUT, stdout=PIPE, shell=True)
                data = p.communicate()[0]
                ret.append(data)
            return render_to_response("ansible/result.html", locals())
        else:
            for h in host:
                for p in pbook:
                    f = open(ansible_dir + '/pbook/' + p, 'r+')
                    flist = f.readlines()
                    flist[0] = '- hosts: '+h+'\n'
                    f = open(ansible_dir + '/pbook/' + p, 'w+')
                    f.writelines(flist)
                    f.close()
                    cmd = "ansible-playbook"+" "+ ansible_dir + '/pbook/' + p
                    p = Popen(cmd, stdout=PIPE, shell=True)
                    data = p.communicate()[0]
                    print data
                    ret.append(data)
            return render_to_response('ansible/result.html', locals())
