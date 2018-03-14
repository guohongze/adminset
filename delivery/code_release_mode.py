# -*- coding: utf-8 -*-
from .nginx import Config_Update
import os
from .file_lib import loginfo_to_file
from .ansible_api import Ansible_cmd
from .network_api import host_network_probe
import time

def code_release(host_group,lvs_group,config_path,dest_path,lvs_name,logfile,code_src,code_dest,java_script,work_path,obj_name,exclude=None):
    """代码发布模块"""
    if isinstance(host_group, str):
        host_name_s = [host_group]
    else:
        host_name_s = host_group
    lvs_config = Config_Update(config_path,host_name_s)
    # 注解发布代码主机地 负载均衡配置
    aa = lvs_config.annotation_file_nginx()
    if len(aa[0]) > 0:
        for I in aa[0]:
            if "Success" in I:
                pass
            else:
                loginfo_to_file(logfile, "<br>".join(aa[0]))
                return False
    else:
        loginfo_to_file(logfile, "<br>".join(aa[0]))
        return False

    kk = lvs_config.config_rsync(lvs_group,aa[1],dest_path,lvs_name)
    if kk[0] == "0":
        pass
    else:
        loginfo_to_file(logfile, kk[1])
        return False
    aaa = "<br>".join(aa[0])
    logig_info = "{0}<br>{1}".format(aaa,kk[1])
    loginfo_to_file(logfile, logig_info)
    code_rsync_dest(host_name_s,code_src,code_dest,java_script,work_path,obj_name,logfile,exclude)
    aa = lvs_config.un_annotation_file_nginx()
    if len(aa[0]) > 0:
        for I in aa[0]:
           if "Success" in I:
                pass
           else:
               loginfo_to_file(logfile, aa[0:])
               return False
    else:
        return False

    lvs_config.config_rsync(lvs_group, aa[1], dest_path, lvs_name)
    if kk[0] == "0":
        pass
    else:
        loginfo_to_file(logfile, kk[1])
        return False
    return True


def code_rsync_dest(host_group,code_src,code_dest,java_script,work_path,obj_name,logfile,exclude=None,):
    ansible_cmd = Ansible_cmd(host_group)
    path_if = ansible_cmd.shell_run("if [ -d {0} ]; then echo 'True'; else echo 'False'; fi".format(code_dest))
    if "True" in path_if:
        return 1
    path_list = "/" + "/".join(code_dest.split("/")[1:-1])
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
    java_run.java_start(java_script)
    loginfo_to_file(logfile, "{0}<br>".format("java start END!"))
    networ_test = host_network_probe(host_group, 8080)
    if "False" in networ_test:
        kkk = 5
        for I in range(6):
            time.sleep(5)
            networ_test = host_network_probe(host_group, 8080)
            if "True" in networ_test:
                break
    loginfo_to_file(logfile, "{0}<br>".format(networ_test))
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

# def script_cmd():



