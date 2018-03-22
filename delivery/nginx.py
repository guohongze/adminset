# -*- coding: utf-8 -*-
import os
from file_lib import find_file, if_file, file_in_str, update_file
from .shell_cmd_api import cmd_exec


nginx_cofnig = "../nginx/nginx.conf"



def open_nginx_condif(nginx_config_file):
    if  if_file(nginx_config_file):
        pass
    else:
        return {"code":1, "info":u"找不到配置文件"}
    dd = ""
    with open(nginx_config_file, 'r') as f:
        for lin in f:
            if not lin.replace(" ","").startswith("#") and "include" in lin and "conf" in lin:
                nginx_path = os.path.dirname(lin).replace("include", "").replace(" ", "")
                nginx_file_name = lin.replace(nginx_path, "").replace(";", "").replace("/", "").replace("include", "")\
                    .replace(" ", "").replace("\n","")
                path_list = os.listdir(os.path.dirname(__file__) + nginx_path)
                file_name = find_file('(\w%s)' % nginx_file_name,  path_list)
                for I in file_name:
                    with open(os.path.dirname(__file__) + nginx_path + "/" + I,'r') as flie:
                        open_file = flie.read()
                        dd += open_file
            else:
                dd += lin
    return dd


class Config_Update(object):
    """nginx配置文件更新"""
    def __init__(self,config_path,keyword_host):
        self.config_path = config_path
        self.keyword_name = keyword_host
        self.if_file = self.__if_file()

    def __if_file(self):
        if os.path.exists(self.config_path):
            pass
        else:
            return {"code":1,"info":u"Undetected configuration file"}
    def __nginx_file_jx(self,nginx_file_path):
        """获取nginx include 引入的配置文件名"""
        with open(nginx_file_path, 'r') as f:
            for lin in f:
                if not lin.replace(" ", "").startswith("#") and "include" in lin and "conf" in lin:
                    n_path = os.path.dirname(lin).replace("include", "").replace(" ", "")
                    nginx_include_name = lin.replace(n_path, "")\
                        .replace(";", "")\
                        .replace("/", "").\
                        replace("include","") \
                        .replace(" ", "")\
                        .replace("\n", "")
                    nginx_pwd = os.path.dirname(os.path.dirname(nginx_file_path)) + "/"
                    nginx_path = os.listdir(nginx_pwd + n_path)
                    file_name = find_file('(\w%s)' % nginx_include_name, nginx_path)
                    dd = []
                    for I in file_name:
                        dd.append(nginx_pwd + n_path + "/" + I)
        return [dd,nginx_pwd + n_path]

    def annotation_file_nginx(self):
        """注解配置文件"""
        include_name = self.__nginx_file_jx(self.config_path)
        dd = []
        for I in include_name[0]:
            if file_in_str(I,self.keyword_name):
                for D in self.keyword_name:
                    update_jg = update_file(I,D,"#annotation_file_","annotation_file")
                if update_jg == 1:
                    dd.append("<br>".join([I,u"config update Success"]))
                else:
                    dd.append("<br>".join([I,u"cofnig update error"]))
        return [dd,include_name[1]]

    def un_annotation_file_nginx(self):
        """取消注解配置文件"""
        include_name = self.__nginx_file_jx(self.config_path)
        dd = []
        for I in include_name[0]:
            if file_in_str(I,self.keyword_name):
                for D in self.keyword_name:
                    update_jg = update_file(I,D,"#annotation_file_","un_annotation_file")
                if update_jg == 1:
                    dd.append("<br>".join([I,u"config update Success"]))
                else:
                    dd.append("<br>".join([I,u"cofnig update error"]))
        return [dd,include_name[1]]

    def config_rsync(self,host_ip,str_path,dest_path,type):
        """同步配置文件"""
        cmd = "rsync --progress -raz --delete --exclude '.git' --exclude '.svn' {0}/ {1}:{2}".format(
            str_path, host_ip, dest_path)
        cmd_exec(cmd)
        if type == "nginx":
            cmd_ansible_test = "ansible {0} -a 'nginx -t'" .format(host_ip)
            cmd_ansible_reload = "ansible {0} -a 'nginx -s reload'".format(host_ip,
                                                                           type)
        elif type == "haproxy":
            cmd_ansible_test = "ansible {0} -a 'haproxy -c -f {1}'".format(host_ip,
                                                                           dest_path + "haproxy.cfg")
            cmd_ansible_reload = "ansible {0} -a 'service haproxy reload'".format(host_ip,
                                                                                  type,
                                                                                  dest_path + "haproxy.cfg")
        else:
            return  ["1","error"]
        cmd_return = cmd_exec(cmd_ansible_test)

        if "Configuration file is valid" in cmd_return or "test is successful" in cmd_return:
            pass
        else:
            return ["1","{0} Configuration file exception！".format(type)]
        cmd_return = cmd_exec(cmd_ansible_reload)
        return ["0",cmd_return]



if __name__ == "__main__":
    ccc =  Config_Update(nginx_cofnig,"sadasdadasdasdasd")
    dd = ccc.un_annotation_file_nginx()
    print(dd)









