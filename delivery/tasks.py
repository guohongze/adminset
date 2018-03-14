#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Delivery
import os
import shutil
from time import sleep
import re
import sh, time
from .nginx import *
from .haproxy import *
from .code_release_mode import code_release
from .ansible_api import Ansible_cmd
from .code_release_mode import code_rsync_dest


@shared_task
def deploy(job_name, server_list, app_path, source_address, project_id, auth_info):
    cmd = ""
    p1 = Delivery.objects.get(job_name_id=project_id)
    job_workspace = "/var/opt/adminset/workspace/{0}/".format(job_name)
    log_path = job_workspace + 'logs/'
    log_name = 'deploy-' + str(p1.deploy_num) + ".log"
    with open(log_path + log_name, 'wb+') as f:
        f.writelines("<h4>Deploying project {0} for {1}th</h4>".format(job_name, p1.deploy_num))
    if not app_path.endswith("/"):
        app_path += "/"

    # clean build code
    p1.bar_data = 20
    p1.save()
    sleep(1)
    if p1.build_clean or p1.version:
        try:
            shutil.rmtree("{0}code/".format(job_workspace))
        except BaseException as msg:
            print("code dir is not exists, build clean over")
    if p1.job_name.source_type == "git":
        cmd = git_clone(job_workspace, auth_info, source_address, p1)
    if p1.job_name.source_type == "svn":
        cmd = svn_clone(job_workspace, auth_info, source_address, p1)
    data = cmd_exec(cmd)
    p1.bar_data = 30
    p1.save()
    with open(log_path + log_name, 'ab+') as f:
        f.writelines(cmd)
        f.writelines(data)
    if p1.shell:
        deploy_shell = job_workspace + 'scripts/deploy-' + str(p1.deploy_num) + ".sh"
        deploy_shell_name = 'deploy-' + str(p1.deploy_num) + ".sh"
        with open(deploy_shell, 'wb+') as f:
            f.writelines(p1.shell)
        cmd = "/usr/bin/dos2unix {}".format(deploy_shell)
        data = cmd_exec(cmd)
    for server in server_list:
        cmd = "rsync --progress -raz --delete --exclude '.git' --exclude '.svn' {0}/code/ {1}:{2}".format(
                job_workspace, server, app_path)
        data = cmd_exec(cmd)
        with open(log_path + log_name, 'ab+') as f:
            f.writelines(cmd)
            f.writelines(data)
        if p1.shell and not p1.shell_position:
            cmd = "scp {0} {1}:/tmp".format(deploy_shell, server)
            data = cmd_exec(cmd)
            with open(log_path + log_name, 'ab+') as f:
                f.writelines(data)
            cmd = "ssh {1} '/usr/bin/bash /tmp/{0}'".format(deploy_shell_name, server)
            data = cmd_exec(cmd)
            with open(log_path + log_name, 'ab+') as f:
                f.writelines(data)
        if p1.bar_data <= 125:
            cur_bar = p1.bar_data
            p1.bar_data = cur_bar+5
            p1.save()
    if p1.shell and p1.shell_position:
        # cmd = "/usr/bin/bash {0}'".format(deploy_shell)
        data = sh.bash(deploy_shell)
        with open(log_path + log_name, 'ab+') as f:
            f.writelines(data)
    p1.bar_data = 130
    p1.status = False
    p1.save()
    with open(log_path + log_name, 'ab+') as f:
        f.writelines("<h4>Project {0} have deployed for {1}th </h4>".format(p1.job_name, p1.deploy_num))
    return data

@shared_task
def new_deploy(job_name, server_list, app_path, source_address, project_id, auth_info):
    opt = locals()
    server_list_len = 0
    code_tongbu = []

    def baocuen(bar_data,status):
        p1.bar_data = bar_data
        p1.status = status
        p1.save()

    for key in opt:
        if opt[key] == None and key != "auth_info":
            return "%s is None" % key
    cmd = ""
    p1 = Delivery.objects.get(job_name_id=project_id)
    print p1.job_name.raync_exclude
    job_workspace = "/var/opt/adminset/workspace/{0}/".format(job_name)
    log_path = job_workspace + 'logs/'
    log_name = 'deploy-' + str(p1.deploy_num) + ".log"
    with open(log_path + log_name, 'wb+') as f:
        f.writelines("<h4>Deploying project {0} for {1}th</h4>".format(job_name, p1.deploy_num))
    if not app_path.endswith("/"):
        app_path += "/"

    if p1.job_name.source_type == "git":
        cmd = git_clone(job_workspace,
                        auth_info,
                        source_address,
                        p1)
    if p1.job_name.source_type == "svn":
        cmd = svn_clone(job_workspace,
                        auth_info,
                        source_address,
                        p1)
    data = cmd_exec(cmd)
    p1.bar_data = 30
    p1.save()

    with open(log_path + log_name, 'ab+') as f:
        f.writelines(cmd)
    with open(log_path + log_name, 'ab+') as f:
        f.writelines("<br>")
    with open(log_path + log_name, 'ab+') as f:
        f.writelines(data)

    if isinstance(server_list, list) and len(server_list) > 1:
        server_list_1 = server_list[:int(len(server_list) / 2)]
        server_list_2 = server_list[(len(server_list) / 2):]
        server_list_len = 2
    else:
        server_list_len = 1
        server_list_1 = server_list

    #分批发布代码
    if server_list_len == 2:
        # 第一组主机
        lvs_zhuji = code_release(host_group=server_list_1,
                                 lvs_group=p1.job_name.lvs_host_ip,
                                 config_path=p1.job_name.configPath,
                                 dest_path=p1.job_name.lvs_cofnig_path,
                                 lvs_name=p1.job_name.lvs_type,
                                 logfile=log_path + log_name,
                                 code_src="{0}/code/".format(job_workspace),
                                 code_dest="/war/{0}/{1}".format(p1.job_name.appPath,
                                                                 time.strftime("%Y%m%d-%H%M%S", time.localtime())
                                                                 ),
                                 java_script=p1.job_name.java_script,
                                 work_path=p1.job_name.appPath,
                                 obj_name=p1.job_name.name,
                                 exclude=p1.job_name.raync_exclude)
        if lvs_zhuji:
            baocuen(60,True)
        else:
            baocuen(60, False)
            return 1
        with open(log_path + log_name, 'ab+') as f:
            f.writelines("<br><h5>Deploying project {0} for {1}th</h5>".format(job_name, p1.deploy_num))
        #第二组主机
        lvs_zhuji = code_release(host_group=server_list_2,
                                 lvs_group=p1.job_name.lvs_host_ip,
                                 config_path=p1.job_name.configPath,
                                 dest_path=p1.job_name.lvs_cofnig_path,
                                 lvs_name=p1.job_name.lvs_type,
                                 logfile=log_path + log_name,
                                 code_src="{0}/code/".format(job_workspace),
                                 code_dest="/war/{0}/{1}".format(p1.job_name.appPath,
                                                                 time.strftime("%Y%m%d-%H%M%S", time.localtime())
                                                                 ),
                                 java_script=p1.job_name.java_script,
                                 work_path=p1.job_name.appPath,
                                 obj_name=p1.job_name.name,
                                 exclude=p1.job_name.raync_exclude)
        if lvs_zhuji:
            baocuen(130, True)
        else:
            baocuen(130, False)
            return 1
    elif server_list_len == 1:
        # ansible_cmd = Ansible_cmd(server_list_1)
        # ansible_shell = ansible_cmd.rsycn(job_workspace + "/code/", "/opt/")
        # if ansible_shell[0] == "1":
        #     with open(log_path + log_name, 'wb+') as f:
        #         f.writelines("<h4>{0}</h4>".format(ansible_shell[1]))
        #     baocuen(130, False)
        #     return 1
        # else:
        #     with open(log_path + log_name, 'wb+') as f:
        #         f.writelines("<h4>{0}</h4>".format(ansible_shell[1]))
        code_rsync_dest(host_group=server_list_1,
                        code_src="{0}/code/".format(job_workspace),
                        code_dest="/war/{0}/{1}".format(p1.job_name.appPath,
                                                        time.strftime("%Y%m%d-%H%M%S", time.localtime())
                                                        ),
                        java_script=p1.job_name.java_script,
                        work_path=p1.job_name.appPath,
                        obj_name=p1.job_name.name,
                        logfile=log_path + log_name,
                        exclude=p1.job_name.raync_exclude)

    else:
        baocuen(130, False)
        with open(log_path + log_name, 'ab+') as f:
            f.writelines("<h4>No host IP addess!</h4>")
    baocuen(130, False)
    with open(log_path + log_name, 'ab+') as f:
        f.writelines("<h4>Project {0} have deployed for {1}th</h4>".format(p1.job_name, p1.deploy_num))
    return code_tongbu

def parser_url(source_address, url_len, user_len, auth_info, url_type=None):
    if url_type:
        new_suffix = source_address[url_len:][user_len:]
        final_add = source_address[:url_len] + auth_info["username"] + ":" + auth_info["password"] + new_suffix
    else:
        new_suffix = source_address[url_len:]
        final_add = source_address[:url_len] + auth_info["username"] + ":" + auth_info["password"] + new_suffix
    return final_add

def git_clone(job_workspace, auth_info, source_address, p1):
    if os.path.exists("{0}code/{1}/.git".format(job_workspace,p1.job_name.name)):
        cmd = "cd {0}code/{1} && git pull".format(job_workspace,p1.job_name.name)
        return cmd
    if not os.path.exists("{0}/code/{1}".format(job_workspace,p1.job_name.name)):
        os.makedirs("{0}/code/{1}".format(job_workspace,p1.job_name.name))
        print "{0}/code/{1}".format(job_workspace,p1.job_name.name)
    # if auth_info and p1.job_name.source_address.startswith("http"):
    #     url_type = re.search(r'(@)', source_address)
    #     if url_type:
    #         user_len = len(auth_info["username"])
    #         if source_address.startswith("https://"):
    #             url_len = 8
    #         else:
    #             url_len = 7
    #         source_address = parser_url(source_address, url_len, user_len, auth_info, url_type)
    #     else:
    #         if source_address.startswith("https://"):
    #             url_len = 8
    #         else:
    #             url_len = 7
    #         source_address = parser_url(source_address, url_len, auth_info, url_type)
    if p1.version:
        cmd = "git clone {0} {1}code/{3}/".format(source_address, job_workspace, p1.version,p1.job_name.name)
    else:
        cmd = "git clone {0} {1}code/{2}".format(source_address, job_workspace,p1.job_name.name)
    return cmd


def svn_clone(job_workspace, auth_info, source_address, p1):
    if p1.version:
        if not source_address.endswith("/") and not p1.version.endswith('/'):
            source_address += '/'
        source_address += p1.version
    if os.path.exists("{0}code/.svn".format(job_workspace)):
        cmd = "svn --non-interactive --trust-server-cert --username {2} --password {3} update {0} {1}code/".format(
                source_address, job_workspace, auth_info["username"], auth_info["password"])
    else:
        cmd = "svn --non-interactive --trust-server-cert --username {2} --password {3} checkout {0} {1}code/".format(
                source_address, job_workspace, auth_info["username"], auth_info["password"])
    return cmd


def del_build_code(path):
    """清理原有发布的生成的代码"""
    try:
        shutil.rmtree("{0}code/".format(path))
        return ["{0}code/".format(path),"success",0]
    except StandardError as msg:
        return ["{0}code/".format(path), "path file None or file Non permissions deleting",1]


def code_release_1(server_list,jow_workspace,app_path,auth_info=None,p_number=5):
    cmd_data = []
    for I in server_list:
        cmd = "rsync --progress -raz --delete --exclude '.git' --exclude '.svn' {0}/code/ {1}:{2}".format(
            jow_workspace, I, app_path)
        data = cmd_exec(cmd)
        cmd_data.append(data)
    return cmd_data

