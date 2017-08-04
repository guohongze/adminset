#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE


def deploy_key(ip, ssh_pwd):
    cmd = "/usr/bin/expect /var/opt/adminset/main/lib/sshkey_deploy {} {}".format(ip, ssh_pwd)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    data = p.communicate()
    return data
