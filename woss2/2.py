#! /usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import time
r = redis.StrictRedis(host='192.168.47.100', port=6379, db=0)

def recount():
    i=3000
    while i > 1:
        stime = time.time()
        r.get("foo")
        etime = time.time()
        times = etime - stime
        s = str(times)
        #f = open('rediscount.txt', 'a')
        now = time.time()
        str1 = str(now)
        str3 = str1+" "+s#+"\n"
        print str3
        #f.write(str3

timed = int(time.time())
while True:
    if timed < int(time.time())-1:
        recount()


