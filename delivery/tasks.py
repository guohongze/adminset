#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from subprocess import Popen, PIPE
from delivery.models import Delivery
import os
import shutil
from time import sleep, ctime
import re
import sh


@shared_task
def deploy(job_name, server_list, app_path, source_address, project_id, auth_info, rsync_status, source_auth):
    cmd = ""
    try:
        username = auth_info["username"]
        deploy_port = auth_info["deploy_port"]
    except:
        username = "root"
        deploy_port = 22

    p1 = Delivery.objects.get(job_name_id=project_id)
    job_workspace = "/var/opt/adminset/workspace/{0}/".format(job_name)
    log_path = job_workspace + 'logs/'
    log_name = 'deploy-' + str(p1.deploy_num) + ".log"
    with open(log_path + log_name, 'wb+') as f:
        f.writelines("<h4>Deploying Project {0} For {1} Th</h4>\n".format(job_name, p1.deploy_num))
        f.writelines("Code version: {0}".format(p1.version))
        f.writelines("\n")
        f.writelines("Deploy time: {0}".format(ctime()))
        f.writelines("\n\n")
    if not app_path.endswith("/"):
        app_path += "/"

    # clean build code
    p1.bar_data = 20
    p1.save()
    sleep(1)
    if p1.build_clean or p1.version:
        try:
            with open(log_path + log_name, 'ab+') as f:
                f.writelines("******STEP: CLEAN PREVIOUS BUILDS******\n")
            shutil.rmtree("{0}code/".format(job_workspace))
        except Exception as msg:
            print("code dir is not exists, build clean over")

    with open(log_path + log_name, 'ab+') as f:
        f.writelines("******STEP: GIT SOURCE CODE******\n\n")

    if source_auth:
        git_auth = auth_info
    else:
        git_auth = None
    if p1.job_name.source_type == "git":
        cmd = git_clone(job_workspace, git_auth, source_address, p1)
    if p1.job_name.source_type == "svn":
        cmd = svn_clone(job_workspace, git_auth, source_address, p1)
    data = cmd_exec(cmd)
    p1.bar_data = 30
    p1.save()
    with open(log_path + log_name, 'ab+') as f:
        f.writelines(cmd+"\n")
        f.writelines(data)
        f.writelines("\n")
    if p1.shell:
        with open(log_path + log_name, 'ab+') as f:
            f.writelines("******STEP: DEPLOY SHELL EXECUTE******\n\n")
        deploy_shell = job_workspace + 'scripts/deploy-' + str(p1.deploy_num) + ".sh"
        deploy_shell_name = 'deploy-' + str(p1.deploy_num) + ".sh"
        with open(deploy_shell, 'wb+') as f:
            f.writelines(p1.shell)
        cmd = "/bin/dos2unix {}".format(deploy_shell)
        data = cmd_exec(cmd)
    exclude_file = "{0}/code/exclude.txt".format(job_workspace)
    with open(log_path + log_name, 'ab+') as f:
        f.writelines("******STEP: RSYNC CODE TO SERVER******\n")
    if rsync_status:
        r_code = "--delete"
    else:
        r_code = "--verbose"
    for server in server_list:
        #mkdir app_path
        try:
            sh.ssh("-p {0}".format(deploy_port), "{1}@{0}".format(server, username),
                   "ls {0}".format(app_path))
        except:
            sh.ssh("-p {0}".format(deploy_port), "{1}@{0}".format(server, username),
                   "mkdir -p {0}".format(app_path))

        with open(log_path + log_name, 'ab+') as f:
            f.writelines("\n+++rsync code to {0} +++\n".format(server))
        if os.path.exists(exclude_file):
            cmd = "rsync -e 'ssh -p {6}' --progress -raz {4} --exclude-from {3} {0}/code/ {5}@{1}:{2}".format(
                    job_workspace, server, app_path, exclude_file, r_code, username, deploy_port)
        else:
            cmd = "rsync -e 'ssh -p {5}' --progress -raz {3} --exclude '.git' --exclude '.svn' {0}/code/ {4}@{1}:{2}".format(
                    job_workspace, server, app_path, r_code, username, deploy_port)
        data = cmd_exec(cmd)
        with open(log_path + log_name, 'ab+') as f:
            f.writelines(cmd)
            f.writelines(data)
        if p1.shell and not p1.shell_position:
            with open(log_path + log_name, 'ab+') as f:
                f.writelines("******STEP: SHELL EXECUTE ON REMOTE******\n\n")
            cmd = "scp -P {3} {0} {2}@{1}:/tmp".format(deploy_shell, server, username, deploy_port)
            data = cmd_exec(cmd)
            with open(log_path + log_name, 'ab+') as f:
                f.writelines(data)
            cmd = "ssh -p {3} {2}@{1} '/bin/bash /tmp/{0}'".format(deploy_shell_name, server, username, deploy_port)
            data = cmd_exec(cmd)
            with open(log_path + log_name, 'ab+') as f:
                f.writelines(data)
        if p1.bar_data <= 125:
            cur_bar = p1.bar_data
            p1.bar_data = cur_bar+5
            p1.save()
    if p1.shell and p1.shell_position:
        with open(log_path + log_name, 'ab+') as f:
            f.writelines("******STEP: SHELL EXECUTE ON ADMINSET LOCAL SERVER******\n\n")
        # cmd = "/usr/bin/bash {0}'".format(deploy_shell)
        data = sh.bash(deploy_shell)
        with open(log_path + log_name, 'ab+') as f:
            f.writelines(data)
    p1.bar_data = 130
    p1.status = False
    p1.save()
    with open(log_path + log_name, 'ab+') as f:
        f.writelines("<h4>Project {0} Have Deployed For {1}Th </h4>".format(p1.job_name, p1.deploy_num))
    return data


def cmd_exec(cmd):
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    data = p.communicate()
    return data


def parser_url(source_address, url_len, user_len, auth_info, url_type=None):
    if url_type:
        new_suffix = source_address[url_len:][user_len:]
        final_add = source_address[:url_len] + auth_info["username"] + ":" + auth_info["password"] + new_suffix
    else:
        new_suffix = source_address[url_len:]
        final_add = source_address[:url_len] + auth_info["username"] + ":" + auth_info["password"] + new_suffix
    return final_add


def git_clone(job_workspace, auth_info, source_address, p1):
    if os.path.exists("{0}code/.git".format(job_workspace)):
        cmd = "cd {0}code/ && git pull".format(job_workspace)
        return cmd
    if auth_info and p1.job_name.source_address.startswith("http"):
        url_type = re.search(r'(@)', source_address)
        if url_type:
            user_len = len(auth_info["username"])
            if source_address.startswith("https://"):
                url_len = 8
            else:
                url_len = 7
            source_address = parser_url(source_address, url_len, user_len, auth_info, url_type)
        else:
            if source_address.startswith("https://"):
                url_len = 8
            else:
                url_len = 7
            source_address = parser_url(source_address, url_len, auth_info, url_type)
    if p1.version:
        cmd = "git clone -b {2} {0} {1}code/".format(source_address, job_workspace, p1.version)
    else:
        cmd = "git clone {0} {1}code/".format(source_address, job_workspace)
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
