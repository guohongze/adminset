#!/usr/bin/python
#-*- coding:utf-8 -*-

import platform

def getHostInfo():
    pd ={}
    version = platform.dist()
    os_name = platform.node()
    os_release = platform.release()
    os_version = '%s %s' % (version[0],version[1])
    pd['os_name'] = os_name
    pd['os_release'] = os_release
    pd['os_version'] = os_version
    return pd

if __name__ == '__main__':
    print getHostInfo()
