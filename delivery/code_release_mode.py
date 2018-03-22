# -*- coding: utf-8 -*-
from .nginx import Config_Update
import logging
from lib.log import log
from config.views import get_dir
from .file_lib import loginfo_to_file, str_to_list
from .ansible_api import Ansible_cmd
from .network_api import host_network_probe
import time

scripts_dir = get_dir("s_path")
level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)

def code_release(host_group,lvs_group,config_path,dest_path,lvs_name,logfile,code_src,code_dest,java_script,work_path,obj_name,shell_file=None,exclude=None):
    """代码发布模块"""
    host_group = str_to_list(host_group)
    new_lvs = lvs_update(config_path=config_path,
                         host_group=host_group,
                         logfile=logfile,
                         lvs_group=lvs_group,
                         dest_path=dest_path,
                         lvs_name=lvs_name)
    if not new_lvs:
        return u"负载均衡更新失败"

    code_rsync_dest(host_group, code_src, code_dest, java_script, work_path, obj_name, logfile, shell_file, exclude)

    new_lvs = lvs_update(config_path=config_path,
                         host_group=host_group,
                         logfile=logfile,
                         lvs_group=lvs_group,
                         dest_path=dest_path,
                         lvs_name=lvs_name)
    if not new_lvs:
        return u"负载均衡更新失败"
    return True


def code_rsync_dest(host_group,code_src,code_dest,java_script,work_path,obj_name,logfile,shell_file=None,exclude=None,):
    ansible_cmd = Ansible_cmd(host_group)
    #path_if = ansible_cmd.shell_run("if [ -d {0} ]; then echo 'True'; else echo 'False'; fi".format(code_dest))
    path_list = "/{0}".format("/".join(code_dest.split("/")[1:-1]))
    path_fu = ansible_cmd.shell_run("if [ -d {0} ]; thon echo 'True'; else echo 'False'; fi".format(path_list))
    if "False" in path_fu:
        ansible_cmd.shell_run("mkdir -p {0}".format(path_list))
        loginfo_to_file(logfile,"mkdir {0}".format(path_list))

    java_run = java_shell(host_group)
    java_stop = java_run.java_stop(java_script)
    loginfo_to_file(logfile, "java stop ".format(java_stop))

    loginfo_to_file(logfile, "code rsync start!")
    exclude_list = exclude.split(",")
    rsync_out = ansible_cmd.rsync(code_src,code_dest,exclude=exclude_list)
    loginfo_to_file(logfile, "{0}<br>{1}".format(rsync_out,"code rsync END!"))

    ln_tmp_to_wok(code_dest,work_path,obj_name,host_group)
    loginfo_to_file(logfile, "{0}<br>".format("ln code_dir to wok_dir END!"))

    if shell_file != None and shell_file != "":
        ansible_cmd.shell_script(logfile=logfile, script_cmd=shell_file)

    java_run.java_start(java_script)
    loginfo_to_file(logfile, "{0}<br>".format("java start END!"))

    networ_test = host_network_probe(host_group, 8080)
    if "False" in networ_test:
        for I in range(6):
            time.sleep(5)
            networ_test = host_network_probe(host_group, 8080)
            if "True" in networ_test:
                break
    loginfo_to_file(logfile, "{0}<br>".format(networ_test))
    time.sleep(1)

    return networ_test

class java_shell(Ansible_cmd):
    def java_start(self,java_script):
        return self.shell_run("{0} start".format(java_script))

    def java_stop(self,java_script):
        return self.shell_run("{0} stop".format(java_script))


def ln_tmp_to_wok(tmp_path,wok_path,obj_name,host_ip):
    if not tmp_path.endswith("/"):
        tmp_path = "{0}/".format(tmp_path)
    if not wok_path.endswith("/"):
        wok_path = "{0}/".format(wok_path)
    if obj_name.endswith("/"):
        obj_name = obj_name.rstrip("/")
    cmd = "ln -sfT {0}{2} {1}{2}".format(tmp_path,wok_path,obj_name)
    shell_cmd = Ansible_cmd(host_ip)
    print shell_cmd.shell_run(cmd)

def lvs_update(config_path,host_group,logfile,lvs_group,dest_path,lvs_name):
    lvs_config = Config_Update(config_path, host_group)
    new_lvs_config = lvs_config.annotation_file_nginx()
    if len(new_lvs_config[0]) > 0:
        for I in new_lvs_config[0]:
            if "Success" not in I:
                loginfo_to_file(logfile, "<br>".join(new_lvs_config[0]))
                return False
    else:
        loginfo_to_file(logfile, "<br>".join(new_lvs_config[0]))
        return False
    new_config_rsync = lvs_config.config_rsync(lvs_group, new_lvs_config[1], dest_path, lvs_name)
    if new_config_rsync[0] != "0":
        loginfo_to_file(logfile, new_config_rsync[1])
        return False
    loginfo_to_file(logfile, "{0}<br>{1}".format("<br>".join(new_lvs_config[0]),
                                                 new_config_rsync[1]))
    return True





