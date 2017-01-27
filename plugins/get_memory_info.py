#!/usr/bin/python
#-*- coding:utf-8 -*-

from subprocess import PIPE,Popen
import re
import sys

def getMemInfo():
    p = Popen(['dmidecode'],shell=False,stdout=PIPE)
    stdout, stderr = p.communicate()
    return stdout.strip()

def parserMemInfo(memdata):
    line_in = False
    mem_str = ''
    pd = {}
    fd = {}
    for line in memdata.split('\n'):
        if line.startswith('Memory Device') and line.endswith('Memory Device'):
            line_in = True
            mem_str+='\n'
            continue
        if line.startswith('\t') and line_in:
            mem_str+=line
        else:
            line_in = False
    for i in mem_str.split('\n')[1:]:
        lines = i.replace('\t','\n').strip()
        for ln in lines.split('\n'):
            k, v = [i for i in ln.split(':')]
            pd[k.strip()] = v.strip()
        if pd['Size'] != 'No Module Installed':
            mem_info = 'Size:%s  ; Part_Number:%s ; Manufacturer:%s' % (pd['Size'],pd['Part Number'],pd['Manufacturer'])
            for line in mem_info.split('\n'):
                for word in line.split(';'):
                    k, v = [i.strip() for i in word.split(':')]
                    fd[k] = v.strip()
                yield fd

if __name__ == '__main__':
    memdata = getMemInfo()
    for i in  parserMemInfo(memdata):
        print i
