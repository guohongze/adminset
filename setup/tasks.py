#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from subprocess import Popen, PIPE
from cmdb.models import Host
import sh, os
from config.views import get_dir
import logging
from lib.log import log
from lib.common import GetRedis
scripts_dir = get_dir("s_path")
ansible_dir = get_dir("a_path")
roles_dir = get_dir("r_path")
playbook_dir = get_dir("p_path")
level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)

@shared_task
def command(host, name):
    h = Host.objects.get(hostname=host)
    cmd = sh.ssh("root@"+h.ip, " "+name)
    data = str(cmd)
    return data


@shared_task
def script(host, name):
    h = Host.objects.get(hostname=host)
    sh.scp(scripts_dir+name, "root@"+h.ip+":/tmp/"+name)
    cmd = "ssh root@"+h.ip+" "+'"sh /tmp/{}"'.format(name)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    data = p.communicate()
    return data


@shared_task
def task_exec(request, host, group, pbook, roles, role_vars, write_role_vars):
    ret = []
    r = GetRedis()
    res = r.connect()
    res.set("ansible_status", 1)
    if host:
        if roles:
            if role_vars:
                write_role_vars(roles, role_vars)
            for h in host:
                with open(log_path + "/ansible.log", 'wb+') as f:
                    f.writelines("==========ansible tasks start==========\n")
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
                with open(log_path + "/ansible.log", 'ab+') as f1:
                    f1.writelines(data)
                    f1.writelines("==========ansible tasks end============")
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
        res.set("ansible_status", 0)
        return True

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
        res.set("ansible_status", 0)
        return True