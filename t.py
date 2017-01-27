#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib


def geturl(urls):
    status = urllib.urlopen(urls).code
    print "url check is", status
geturl("http://www.baidu.com")