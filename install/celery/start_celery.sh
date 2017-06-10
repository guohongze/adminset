#!/bin/bash
/usr/bin/celery multi start w1 w2 -c 8 --app=adminset --logfile="/var/opt/adminset/logs/%n%I.log" --pidfile=/var/opt/adminset/pid/%n.pid

