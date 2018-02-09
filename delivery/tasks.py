#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from subprocess import Popen, PIPE
from .models import Delivery
import os
import shutil
from time import sleep

# class GetRedis(object):
#     host = get_dir("redis_host")
#     port = get_dir("redis_port")
#     db = get_dir("redis_db")
#     password = get_dir("redis_password")
#
#     def connect(self):
#         conn = redis.StrictRedis(host=self.host, port=self.port,
#                                  password=self.password, db=self.db)
#         return conn


@shared_task
def deploy(job_name, server_list, app_path, source_address, project_id):
    ret = []
    p1 = Delivery.objects.get(job_name_id=project_id)
    job_workspace = "/var/opt/adminset/workspace/{0}/".format(job_name)
    log_file = job_workspace + 'logs/deploy-' + str(p1.deploy_num) + ".log"
    if app_path.endswith("/"):
        app_path += "/"
    # clean build code
    p1.bar_data = 20
    p1.save()
    sleep(3)
    cmd = ""
    if p1.build_clean:
        try:
            shutil.rmtree("{0}code/".format(job_workspace))
        except:
            print "dir is not exists"
    if p1.job_name.SOURCE_TYPE == "git":
        if os.path.exists("{0}code/.git".format(job_workspace)):
            cmd = "cd {0}code/ && git pull".format(job_workspace)
        else:
            cmd = "git clone {0} {1}code/".format(source_address, job_workspace)
    if p1.job_name.SOURCE_TYPE == "svn":
        if os.path.exists("{0}code/.svn".format(job_workspace)):
            cmd = "cd {0}code/ && svn update".format(job_workspace)
        else:
            cmd = "svn checkout {0} {1}code/".format(source_address, job_workspace)
    if p1.job_name.SOURCE_TYPE == "file":
        os.remove("{0}code/*".format(job_workspace))
        cmd = "cd {1}code/ && wget {0} ".format(source_address, job_workspace)
    p1.bar_data = 30
    p1.save()
    sleep(5)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    data = p.communicate()
    with open(log_file, 'w+') as f:
        f.writelines(data)
    for server in server_list:
        cmd = "rsync --progress -raz --delete --exclude '.git' --exclude '.svn' {0}/code/ {1}:{2}".format(
                job_workspace, server, app_path)
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        data = p.communicate()
        with open(log_file, 'a+') as f:
            f.writelines(data)
        p1.bar_data += 1
        p1.save()
        sleep(4)

    with open(log_file, 'a+') as f:
        f.writelines("{0} Deploy End".format(job_name))
    p1.bar_data = 13
    p1.save()
    sleep(2)
    p1.status = False
    p1.save()
    return data
