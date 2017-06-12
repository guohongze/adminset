#!/usr/bin/python
# coding=utf-8

import os
from subprocess import Popen, PIPE
import re
import urllib
import urllib2
import platform
import socket
import psutil
import time
import schedule

token = 'HPcWR7l4NJNJ'
server_url = 'http://192.168.47.130/cmdb/collect'


def get_ip():
    hostname = socket.getfqdn(socket.gethostname())
    ipaddr = socket.gethostbyname(hostname)
    return ipaddr


def get_dmi():
    p = Popen('dmidecode', stdout=PIPE, shell=True)
    stdout, stderr = p.communicate()
    return stdout


def parser_dmi(dmidata):
    pd = {}
    line_in = False
    for line in dmidata.split('\n'):
        if line.startswith('System Information'):
             line_in = True
             continue
        if line.startswith('\t') and line_in:
                 k,v = [i.strip() for i in line.split(':')]
                 pd[k] = v
        else:
            line_in = False
    return pd


def get_mem_total():
    cmd = "grep MemTotal /proc/meminfo"
    p = Popen(cmd, stdout=PIPE, shell = True)
    data = p.communicate()[0]
    mem_total = data.split()[1]
    memtotal = int(round(int(mem_total)/1024.0/1024.0, 0))
    return memtotal


def get_cpu_model():
    cmd = "cat /proc/cpuinfo"
    p = Popen(cmd, stdout=PIPE, stderr = PIPE, shell = True)
    stdout, stderr = p.communicate()
    return stdout


def get_cpu_cores():
    cpu_cores = {"logical": psutil.cpu_count(logical=False), "physical": psutil.cpu_count()}
    return cpu_cores


def parser_cpu(stdout):
    groups = [i for i in stdout.split('\n\n')]
    group = groups[-2]
    cpu_list = [i for i in group.split('\n')]
    cpu_info = {}
    for x in cpu_list:
        k, v = [i.strip() for i in x.split(':')]
        cpu_info[k] = v
    return cpu_info


def get_disk_info():
    ret = {}
    disk_dev = re.compile(r'Disk\s/dev/sd[a-z]{1}')
    disk_name = re.compile(r'/dev/sd[a-z]{1}')
    pcmd = Popen(['fdisk', '-l'], shell=False,stdout=PIPE)
    stdout, stderr = pcmd.communicate()
    for i in stdout.split('\n'):
        disk = re.match(disk_dev,i)
        if disk:
            dk = re.search(disk_name, disk.group()).group()
            n = Popen('smartctl -i %s' % dk, shell=True, stdout=PIPE)
            p = n.communicate()
            ret[dk] = p
    return ret


def parser_disk_info(diskdata):
    pd = {}
    disknum = diskdata.keys()
    user_capacity = re.compile(r'(User Capacity):(\s+[\d,]{1,50})')
    for num in disknum:
        t = str(diskdata[num])
        for line in t.split('\n'):
            user = re.search(user_capacity, line)
            if user:
                diskvo = user.groups()[1].strip()
                nums = int(diskvo.replace(',', ''))
                endnum = str(nums/1000/1000/1000)
                pd[num] = endnum
    return pd


def post_data(data):
    postdata = urllib.urlencode(data)
    req = urllib2.urlopen(server_url, postdata)
    req.read()
    return True


def main():
    data_info = dict()
    data_info['memory'] = get_mem_total()
    data_info['disk'] = parser_disk_info(get_disk_info())
    cpuinfo = parser_cpu(get_cpu_model())
    cpucore = get_cpu_cores()
    data_info['cpu_num'] = cpucore['logical']
    data_info['cpu_physical'] = cpucore['physical']
    data_info['cpu_model'] = cpuinfo['model name']
    data_info['ip'] = get_ip()
    data_info['sn'] = parser_dmi(get_dmi())['Serial Number']
    data_info['vendor'] = parser_dmi(get_dmi())['Manufacturer']
    data_info['product'] = parser_dmi(get_dmi())['Version']
    data_info['osver'] = platform.linux_distribution()[0] + " " + platform.linux_distribution()[1] + " " + platform.machine()
    data_info['hostname'] = platform.node()
    data_info['token'] = token
    return data_info


def agent_post():
    osenv = os.environ["LANG"]
    os.environ["LANG"] = "us_EN.UTF8"
    result = main()
    os.environ["LANG"] = osenv
    print 'Get the hardwave and softwave infos from host:'
    print result
    print '----------------------------------------------------------'
    post_data(result)
    print 'Post the hardwave and softwave infos to CMDB successfully!'


if __name__ == "__main__":
    schedule.every(10).seconds.do(agent_post)
    while True:
        schedule.run_pending()
        time.sleep(1)
