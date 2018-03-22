#!/usr/bin/env python
# coding=utf-8

import os
from subprocess import Popen, PIPE
import re
import platform
import socket
import time
import json
import threading

token = 'HPcWR7l4NJNJ'
server_ip = '192.168.47.130'

try:
    import psutil
except ImportError as msg:
    print(msg)
    print("----------------------------------------------")
    print("begining install psutil module, please waiting")
    p = Popen('pip install psutil==5.2.2', stdout=PIPE, shell=True)
    stdout, stderr = p.communicate()
    print stdout
    import psutil

try:
    import schedule
except ImportError as msg:
    print msg
    print("------------------------------------------------")
    print("begining install schedule module, please waiting")
    p = Popen('pip install schedule==0.4.3', stdout=PIPE, shell=True)
    stdout, stderr = p.communicate()
    print stdout
    import schedule

try:
    import requests
except ImportError as msg:
    print msg
    print("------------------------------------------------")
    print("begining install schedule module, please waiting")
    p = Popen('pip install requests==2.17.3', stdout=PIPE, shell=True)
    stdout, stderr = p.communicate()
    print stdout
    import requests


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
    cpu_cores = {"physical": psutil.cpu_count(logical=False) if psutil.cpu_count(logical=False) else 0, "logical": psutil.cpu_count()}
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
    device_model = re.compile(r'(Device Model):(\s+.*)')
    serial_number = re.compile(r'(Serial Number):(\s+[\d\w]{1,30})')
    firmware_version = re.compile(r'(Firmware Version):(\s+[\w]{1,20})')
    user_capacity = re.compile(r'(User Capacity):(\s+[\d,]{1,50})')
    for num in disknum:
        t = str(diskdata[num])
        for line in t.split('\n'):
            user = re.search(user_capacity,line)
            if user:
                diskvo = user.groups()[1].strip()
                nums = int(diskvo.replace(',',''))
                endnum = str(nums/1000/1000/1000)
                pd[num] = endnum
    return json.dumps(pd)


def post_data(url, data):
    try:
        r = requests.post(url, data)
        if r.text:
            print r.text
        else:
            print("Server return http status code: {0}".format(r.status_code))
    except StandardError as msg:
        print msg
    return True


def asset_info():
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
    return json.dumps(data_info)


def asset_info_post():
    osenv = os.environ["LANG"]
    os.environ["LANG"] = "us_EN.UTF8"
    print 'Get the hardwave infos from host:'
    print asset_info()
    print '----------------------------------------------------------'
    post_data("http://{0}/cmdb/collect".format(server_ip), asset_info())
    os.environ["LANG"] = osenv
    return True


def get_sys_cpu():
    sys_cpu = {}
    cpu_time = psutil.cpu_times_percent(interval=1)
    sys_cpu['percent'] = psutil.cpu_percent(interval=1)
    sys_cpu['lcpu_percent'] = psutil.cpu_percent(interval=1, percpu=True)
    sys_cpu['user'] = cpu_time.user
    sys_cpu['nice'] = cpu_time.nice
    sys_cpu['system'] = cpu_time.system
    sys_cpu['idle'] = cpu_time.idle
    sys_cpu['iowait'] = cpu_time.iowait
    sys_cpu['irq'] = cpu_time.irq
    sys_cpu['softirq'] = cpu_time.softirq
    sys_cpu['guest'] = cpu_time.guest
    return sys_cpu


def get_sys_mem():
    sys_mem = {}
    mem = psutil.virtual_memory()
    sys_mem["total"] = mem.total/1024/1024
    sys_mem["percent"] = mem.percent
    sys_mem["available"] = mem.available/1024/1024
    sys_mem["used"] = mem.used/1024/1024
    sys_mem["free"] = mem.free/1024/1024
    sys_mem["buffers"] = mem.buffers/1024/1024
    sys_mem["cached"] = mem.cached/1024/1024
    return sys_mem


def parser_sys_disk(mountpoint):
    partitions_list = {}
    d = psutil.disk_usage(mountpoint)
    partitions_list['mountpoint'] = mountpoint
    partitions_list['total'] = round(d.total/1024/1024/1024.0, 2)
    partitions_list['free'] = round(d.free/1024/1024/1024.0, 2)
    partitions_list['used'] = round(d.used/1024/1024/1024.0, 2)
    partitions_list['percent'] = d.percent
    return partitions_list


def get_sys_disk():
    sys_disk = {}
    partition_info = []
    partitions = psutil.disk_partitions()
    for p in partitions:
        partition_info.append(parser_sys_disk(p.mountpoint))
    sys_disk = partition_info
    return sys_disk


# 函数获取各网卡发送、接收字节数
def get_nic():

    key_info = psutil.net_io_counters(pernic=True).keys()  # 获取网卡名称

    recv = {}
    sent = {}

    for key in key_info:
        recv.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_recv)  # 各网卡接收的字节数
        sent.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_sent)  # 各网卡发送的字节数

    return key_info, recv, sent


# 函数计算每秒速率
def get_nic_rate(func):

    key_info, old_recv, old_sent = func()  # 上一秒收集的数据
    time.sleep(1)
    key_info, now_recv, now_sent = func()  # 当前所收集的数据

    net_in = {}
    net_out = {}

    for key in key_info:
        net_in.setdefault(key, (now_recv.get(key) - old_recv.get(key)) / 1024)  # 每秒接收速率
        net_out.setdefault(key, (now_sent.get(key) - old_sent.get(key)) / 1024) # 每秒发送速率

    return key_info, net_in, net_out


def get_net_info():
    net_info = []
    key_info, net_in, net_out = get_nic_rate(get_nic)
    for key in key_info:
        in_data = net_in.get(key)
        out_data = net_out.get(key)
        net_info.append({"nic_name": key, "traffic_in": in_data, "traffic_out": out_data})
    return net_info


def agg_sys_info():

    print 'Get the system infos from host:'
    sys_info = dict()
    sys_info['hostname'] = platform.node()
    sys_info['cpu'] = get_sys_cpu()
    sys_info['mem'] = get_sys_mem()
    sys_info['disk'] = get_sys_disk()
    sys_info['net'] = get_net_info()
    sys_info['token'] = token

    print sys_info
    json_data = json.dumps(sys_info)
    print '----------------------------------------------------------'
    post_data("http://{0}/monitor/received/sys/info/".format(server_ip), json_data)
    return True


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


if __name__ == "__main__":

    asset_info_post()
    time.sleep(1)
    agg_sys_info()
    schedule.every(1800).seconds.do(run_threaded, asset_info_post)
    schedule.every(60).seconds.do(run_threaded, agg_sys_info)
    while True:
        schedule.run_pending()
        time.sleep(1)
