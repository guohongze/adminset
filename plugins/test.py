#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import PIPE,Popen
import re


def getip():
    p = Popen(['ip','addr'],shell=False,stdout=PIPE)
    stdout, stderr = p.communicate()
    return stdout.strip()


def pgetip(ipdata):
    pd = {}
    device = re.compile(r'(eno\d{0,9})')
    ip = re.compile(r'inet ([\d.]{7,15})')
    for lines in ipdata.split('\n'):
        eth_device = re.search(device,lines)
        ips = re.search(ip,lines)
        if eth_device:
            Device = eth_device.groups()
            Ip = ips.groups()[0]
            pd['Device'] = Device
            pd['Ip'] = Ip
            yield pd

def pgetip(ipdata):
    device = re.compile(r'^(eno\d{0,9})')
    mac = re.compile(r'(ether\s[0-9A-Fa-f:]{17})')
    ip = re.compile(r'inet ([\d.]{7,15})')
    for lines in ipdata.split('\n'):
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

pgetip(getip())