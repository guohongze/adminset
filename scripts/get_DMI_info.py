#!/usr/bin/python
# -*- coding:utf-8 -*-

from subprocess import PIPE,Popen
import urllib, urllib2

def getDMI():
    p = Popen('dmidecode',shell=True,stdout=PIPE)
    stdout, stderr = p.communicate()
    return stdout

def parserDMI(dmidata):
    pd = {}
    fd = {}
    line_in = False
    for line in dmidata.split('\n'):
        if line.startswith('System Information'):
            line_in = True
            continue
        if line.startswith('\t') and line_in:
            k, v  = [i.strip() for i in line.split(':')]
            pd[k] = v
        else:
            line_in = False
    name = "Manufacturer:%s ; Serial_Number:%s ; Product_Name:%s" % (pd['Manufacturer'],pd['Serial Number'],pd['Product Name'])
    for i in name.split(';'):
        k, v = [j.strip() for j in i.split(':')]
        fd[k] = v
    return fd

if __name__ == '__main__':
    dmidata = getDMI()
    postdata = parserDMI(dmidata)
    print postdata
