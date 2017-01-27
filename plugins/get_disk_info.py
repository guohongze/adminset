#!/usr/bin/python
#-*- coding:utf-8 -*-

from subprocess import PIPE,Popen
import re

def getDiskInfo():
    disk_dev = re.compile(r'Disk\s/dev/[a-z]{3}')
    disk_name = re.compile(r'/dev/[a-z]{3}')
    p = Popen(['fdisk','-l'],shell=False,stdout=PIPE)
    stdout, stderr = p.communicate()
    for i in stdout.split('\n'):
        disk = re.match(disk_dev,i)
        if disk:
            dk = re.search(disk_name,disk.group()).group()
    n = Popen('smartctl -i %s' % dk,shell=True,stdout=PIPE)
    stdout, stderr = n.communicate()
    return stdout.strip()

def parserDiskInfo(diskdata):
    ld = []
    pd = {}
    device_model = re.compile(r'(Device Model):(\s+.*)')
    serial_number = re.compile(r'(Serial Number):(\s+[\d\w]{1,30})')
    firmware_version = re.compile(r'(Firmware Version):(\s+[\w]{1,20})')
    user_capacity = re.compile(r'(User Capacity):(\s+[\d\w, ]{1,50})')
    for line in diskdata.split('\n'):
        serial = re.search(serial_number,line)
        #print serial
        device = re.search(device_model,line)
        #print device
        firmware = re.search(firmware_version,line)
        #print firmware
        user = re.search(user_capacity,line)
        #print user
        if device:
            pd['Device_Model'] = device.groups()[1].strip()
        if serial:
            pd['Serial_Number'] = serial.groups()[1].strip()
        if firmware:
            pd['Firmware_Version'] = firmware.groups()[1].strip()
        if user:
            pd['User_Capacity'] = user.groups()[1].strip()
    return pd

if __name__ == '__main__':
    diskdata = getDiskInfo()
    print parserDiskInfo(diskdata)
