#!/usr/bin/python
#-*- coding:utf-8 -*-

from subprocess import PIPE,Popen
import re

def getIpaddr():
    p = Popen(['ifconfig'],shell=False,stdout=PIPE)
    stdout, stderr = p.communicate()
    return stdout.strip()

def parserIpaddr(ipdata):
    device = re.compile(r'(wlan\d)')
    ipaddr = re.compile(r'(inet addr:[\d.]{7,15})')
    mac = re.compile(r'(HWaddr\s[0-9A-Fa-f:]{17})')
    link = re.compile(r'(Link encap:[\w]{3,14})')
    mask = re.compile(r'(Mask:[\d.]{9,15})')
    for lines in ipdata.split('\n\n'):
        pd = {}
        eth_device = re.search(device,lines)
        inet_ip = re.search(ipaddr,lines)
        hw = re.search(mac,lines)
        link_encap = re.search(link,lines)
        _mask = re.search(mask,lines)
        if eth_device:
            if eth_device:
                Device = eth_device.groups()[0]
            if inet_ip:
                Ipaddr =  inet_ip.groups()[0].split(':')[1]
            if hw:
                Mac = hw.groups()[0].split()[1]
            if link_encap:
                Link = link_encap.groups()[0].split(':')[1]
            if _mask:
                Mask = _mask.groups()[0].split(':')[1]
            pd['Device'] = Device
            pd['Ipaddr'] = Ipaddr
            pd['Mac'] = Mac
            pd['Link'] = Link
            pd['Mask'] = Mask
            yield pd

if __name__ == '__main__':
    ipdata = getIpaddr()
    for i in parserIpaddr(ipdata):
        print i
