# -*- coding: utf-8 -*-
import os, re
from .shell_cmd_api import cmd_exec


def if_file(file_path):
    """判断文件"""
    if os.path.exists(file_path):
        return True
    else:
        return False

def del_list(list_name):
    """ 删除列表最后一个元素换行符“\n”"""
    list_name2 = []
    if isinstance(list_name,list):
        for I in list_name:
            if I != "\n":
                list_name2.append(I)
    if len(list_name2) > 0:
        ll = list_name2[-1].replace("\n",'')
        list_name2.remove(list_name2[-1])
        list_name2.append(ll)
    return list_name2

def file_show(file_name,str_input,str_output):
    """读取文件，指定关键字开始读取，指定关键字结束"""
    result = []
    flag2, flag = False, False
    with open(file_name, "r") as f:
        for lin in f:
            if lin.replace(' ', '').replace("\n", '') == str_input:
                flag2, flag = True, True
            elif lin.replace(' ', '').startswith(str_output):
                flag = False
                if flag2:
                    break
            if flag:
                result.append(lin)
    return result

def update_file(config_file,Keyword,str_name,update_type):
    """更新文件 注解或取消注解配置文件"""
    find_date = ""
    with open(config_file, "r") as f:
        for lin in f:
            if Keyword in lin:
                if update_type == "annotation_file":
                    if not lin.startswith("#annotation_file_"):
                        new_lin = str_name + lin
                    new_lin = lin
                elif update_type == "un_annotation_file":
                    if lin.startswith("#annotation_file_"):
                        new_lin = lin.replace(str_name, "")
                    new_lin = lin
                else:
                    return "update_type error!"
                lin = lin.replace(lin, new_lin)
            find_date += lin
    with open(config_file, "w") as f:
        f.write(find_date)
    return 1

def find_file(zs,file_parh):
    """根据正则表达式过滤目录下文件文件名，放回列表文件名"""
    if isinstance(file_parh, list):
        pass
    else:
        return file_parh + "type is list"
    ppp = []
    for I in file_parh:
        if re.search(zs, I) != None:
            ppp.append(I)
    return  ppp


def file_in_str(file_name,str_name):
    """判断文件是否包含指定字符"""
    if isinstance(file_name, str):
        pass
    else:
        return file_name + "in str"
    with open(file_name,'r') as f:
        file_open = f.read()
    if isinstance(str_name, list):
        for I in str_name:
            if I in file_open:
                return True
        return False
    else:
        if str_name in file_open:
            return True
        else:
            return False


def loginfo_to_file(log_file,info):
    with open(log_file, "ab+") as f:
        f.writelines("<br><h5>{0}</h5<br>".format(info))
        f.read()
    f.close()

def file_path_zip(src,dest):
    cmd="tar -zcvf {0} {1}".format(src,dest)
    cmd_exec(cmd)



def shell_w_to_file(shell_cmd,shell_path,shell_name,code_path):
    updaet_stc = [
        {"src_tar": "adminset_job_name", "desc_str": shell_name},
        {"src_tar": "adminset_job_path", "desc_str": code_path},
    ]
    for I in updaet_stc:
        shell_cmd = shell_cmd.replace(I["src_tar"], I["desc_str"])
    if not shell_name.endswith(".sh"):
        shell_name = "{0}.sh".format(shell_name)
    if not shell_path.endswith("/"):
        shell_path = "{0}/".format(shell_path)

    shell_path_url = "{0}{1}".format(shell_path,shell_name)

    with open(shell_path_url, "w") as f:
        f.write(shell_cmd)
    cmd_exec("/usr/bin/fromdos {0}".format(shell_path_url))
    return shell_path_url

def str_to_list(input_info):
    if isinstance(input_info, str):
        out_info = [input_info]
    else:
        out_info = input_info
    return out_info


