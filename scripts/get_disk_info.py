#!/usr/bin/python
#-*- coding:utf-8 -*-

from subprocess import PIPE,Popen
import re
import json


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
                pd[num] = nums/1000/1000/1000
    return json.dumps(pd)

if __name__ == '__main__':
    diskdata = getDiskInfo()
    print parserDiskInfo(diskdata)
