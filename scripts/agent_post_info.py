#!/usr/bin/python
#coding=utf-8

import os
from subprocess import Popen, PIPE
import re
import json
import urllib
import urllib2
import platform
import socket

token = 'HPcWR7l4NJNJ'
server_url = 'http://192.168.47.130:8000/cmdb/collect'


def get_ip():
    hostname = socket.getfqdn(socket.gethostname())
    ipaddr = socket.gethostbyname(hostname)
    return ipaddr


def getDMI():
    p = Popen('dmidecode', stdout=PIPE, shell=True)
    stdout, stderr = p.communicate()
    return stdout


def parserDMI(dmidata):
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


def getMemTotal():
    cmd = "grep MemTotal /proc/meminfo"
    p = Popen(cmd, stdout = PIPE, shell = True)
    data = p.communicate()[0]
    mem_total = data.split()[1]
    memtotal = int(round(int(mem_total)/1024.0/1024.0, 0))
    return memtotal


def getCpu():
    cmd = "cat /proc/cpuinfo"
    p = Popen(cmd, stdout = PIPE, stderr = PIPE, shell = True)
    stdout, stderr = p.communicate()
    return stdout


def parserCpu(stdout):
    groups = [i for i in stdout.split('\n\n')]
    group = groups[-2]
    cpu_list = [ i for i in group.split('\n')]
    cpu_info = {}
    for x in cpu_list:
        k, v = [i.strip() for i in x.split(':')]
        cpu_info[k] = v
    return cpu_info


def getDiskInfo():
    ret = {}
    disk_dev = re.compile(r'Disk\s/dev/sd[a-z]{1}')
    disk_name = re.compile(r'/dev/sd[a-z]{1}')
    pcmd = Popen(['fdisk','-l'],shell=False,stdout=PIPE)
    stdout, stderr = pcmd.communicate()
    for i in stdout.split('\n'):
        disk = re.match(disk_dev,i)
        if disk:
            dk = re.search(disk_name,disk.group()).group()
            n = Popen('smartctl -i %s' % dk,shell=True,stdout=PIPE)
            p = n.communicate()
            ret[dk] = p
    return ret


def parserDiskInfo(diskdata):
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
                pd[num] = endnum + 'G'
    return pd


def postData(data):
    postdata = urllib.urlencode(data)
    req = urllib2.urlopen(server_url, postdata)
    req.read()
    return True


def main():
    data_info = {}
    data_info['memory'] = getMemTotal()
    data_info['disk'] = parserDiskInfo(getDiskInfo())
    cpuinfo = parserCpu(getCpu())
    data_info['cpu_num'] = cpuinfo['cpu cores']
    data_info['cpu_model'] = cpuinfo['model name']
    data_info['ip'] = get_ip()
    data_info['sn'] = parserDMI(getDMI())['Serial Number']
    data_info['vendor'] = parserDMI(getDMI())['Manufacturer']
    data_info['product'] = parserDMI(getDMI())['Version']
    os_version = [i for i in platform.linux_distribution()]
    os_version.append(platform.machine())
    os_ver = ''
    for x in os_version:
        os_ver += x
        os_ver = os_ver + ' '
    os_ver = os_ver.rstrip()
    data_info['osver'] = os_ver
    data_info['hostname'] = platform.uname()[1]
    data_info['token'] = token


    return data_info

if __name__ == "__main__":
    osenv = os.environ["LANG"]
    os.environ["LANG"] = "us_EN.UTF8"
    result = main()
    os.environ["LANG"] = osenv
    print 'Get the hardwave and softwave infos from host:'
    print result
    print '----------------------------------------------------------'
    postData(result)
    print 'Post the hardwave and softwave infos to CMDB successfully!'


