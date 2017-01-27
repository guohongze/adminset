#!/usr/bin/python
#coding=utf-8

from subprocess import Popen, PIPE
import re
import urllib
import urllib2
import platform

def getIpaddr():
    p = Popen(['ifconfig'],shell=False,stdout=PIPE)
    stdout, stderr = p.communicate()
    return stdout.strip()


def parserIpaddr(ipdata):
    device = re.compile(r'^(eno\d{0,9})')
    mac = re.compile(r'(ether\s[0-9A-Fa-f:]{17})')
    ip = re.compile(r'inet ([\d.]{7,15})')
    for lines in ipdata.split('\n\n'):
        pd = {}
        eth_device = re.search(device,lines)
        hw = re.search(mac,lines)
        ips = re.search(ip,lines)
        if eth_device:
            if eth_device:
                Device = eth_device.groups()[0]
            if hw:
                Mac = hw.groups()[0].split()[1]
            if ips:
                Ip = ips.groups()[0]
            pd['Device'] = Device
            pd['Mac'] = Mac
            pd['Ip'] = Ip
            yield pd


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
    return mem_total

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

def postData(data):
    postdata = urllib.urlencode(data)
    req = urllib2.urlopen('http://192.168.47.141:8000/cmdb/collect',postdata)
    req.read()
    return True

def main():
    data_info = {}
    """
    data_info = {'ipaddrs':'192.168.3.123','memory':16,'cpu_model':'Intel','cpu_num':4,'sn':'R9NBEZA','vendor':'LENOVO','product':'ThinkPad X220','osver':'Fedora 16 x86_64','hostname':'Sibiao Luo'}
    """
    memtotal = int(round(int(getMemTotal())/1024.0/1024.0, 0))
    data_info['memory'] = memtotal
    
    cpuinfo = parserCpu(getCpu())
    data_info['cpu_num'] = int(cpuinfo['processor']) + 1
    data_info['cpu_model'] = cpuinfo['vendor_id']
    for i in parserIpaddr(getIpaddr()):
        data_info['ip'] = i['Ip']
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

    return data_info

if __name__ == "__main__":
    result = main()
    print 'Get the hardwave and softwave infos from host:'
    print result
    print '----------------------------------------------------------'
    postData(result)
    print 'Post the hardwave and softwave infos to CMDB successfully!'

