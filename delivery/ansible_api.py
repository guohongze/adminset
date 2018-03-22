# -*- coding: utf-8 -*-
import os
from .shell_cmd_api import cmd_exec
from .file_lib import loginfo_to_file


class Ansible_cmd(object):
    def __init__(self,host_ip, forks=5):
        self.host_ip = self.__host_list(host_ip)
        self.forks = forks

    def __host_list(self,host_ip):
        if isinstance(host_ip, list):
            host_group = (",").join(host_ip)
        else:
            host_group = host_ip
        return host_group

    def ping(self):
        shell_cmd = "ansible {0} -f {1} -m ping".format(self.host_ip,self.forks)
        cmd_out = cmd_exec(shell_cmd)
        return cmd_out

    def rsync(self,str_path,dest_path,exclude=None):
        if isinstance(self.host_ip,list):
            host_g = ",".join(self.host_ip)
        else:
            host_g = self.host_ip
        ansible_rsync_opts = [
            'ansible {0} -m synchronize  -a "src={1} dest={2} delete=yes '.format(host_g,str_path,dest_path)
        ]
        rsync_opts = ['rsync_opts=--exclude=.git','--exclude=.gitignore','--exclude=README.md','--exclude=.svn']
        if exclude and isinstance(exclude, list):
            for I in exclude:
                rsync_opts.append("--exclude={0}".format(I))
        new_rsync_opts = ",".join(rsync_opts)
        ansible_rsync_opts.append(new_rsync_opts)
        ansible_rsync_opts.append("\"")
        new_ansible_rsync_opts = " ".join(ansible_rsync_opts)
        cmd_out = cmd_exec(new_ansible_rsync_opts)
        return cmd_out


    def shell_run(self,cmd):
        shell_cmd = "ansible {0} -f {1} -m shell -a \"{2}\"".format(self.host_ip,self.forks,cmd)
        cmd_out = cmd_exec(shell_cmd)
        return cmd_out


    def __shell_copy(self,src_file,dest_file):
        shell_cmd = "ansible {0} -f {1} -m copy -a \"src={2} dest={3}\"".format(self.host_ip,self.forks,src_file,dest_file)
        cmd_exec(shell_cmd)
    def shell_script(self,script_cmd,logfile):
        if script_cmd == "" or script_cmd == None  or not os.path.isfile(script_cmd):
            loginfo_to_file(logfile,"{0} is not file!".format(script_cmd))
        shell_script_cmd = "ansible {0} -f {1} -m script -a \"{2}\"".format(self.host_ip,self.forks,script_cmd)
        cmd_out = cmd_exec(shell_script_cmd)
        loginfo_to_file(logfile,"<br><h5>{0}</h5>".format(cmd_out))
        #print cmd_out