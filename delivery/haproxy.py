# -*- coding: utf-8 -*-
from .file_lib import *

haproxy_config_path = './haproxy.cfg'

def select(arg,haproxy_config_path):
    """查询haproxyp配置文件，输入字段"""
    if if_file(haproxy_config_path):
        pass
    else:
        return u"没有检测到配置文件"
    show_str_name = "listen%s" % arg.replace(' ','')
    name_1 = file_show(haproxy_config_path,show_str_name,"listen")
    return del_list(name_1)

def annotation_file(org,haproxy_config_path):
    """更新haproxyp配置文件，输入字段"""
    if if_file(haproxy_config_path):
        pass
    else:
        return u"没有检测到配置文件"
    dd = update_file(haproxy_config_path, org, "#annotation_file_", "annotation_file")
    if dd == 1:
        return u"更新完成"
    else:
        return u"更新失败"

def un_annotation_file(org,haproxy_config_path):
    """更新haproxyp配置文件，输入字段"""
    if if_file(haproxy_config_path):
        pass
    else:
        return u"没有检测到配置文件"
    dd = update_file(haproxy_config_path,org,"#annotation_file_","un_annotation_file")
    if dd == 1:
        return u"更新完成"
    else:
        return u"更新失败"

if __name__ == "__main__":
    name_url = input("请输入要查询的域名：")
    if name_url != "":
        show_name = annotation_file(name_url)
        if show_name != "":
            print(show_name)
        else:
            print("查询空")
    else:
        print("输入空")