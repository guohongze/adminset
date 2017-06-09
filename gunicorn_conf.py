#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import multiprocessing

path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.split(path_of_current_file)[0]
_file_name = os.path.basename(__file__)
sys.path.insert(0, path_of_current_dir)


worker_class = 'sync'
workers = multiprocessing.cpu_count() * 2 + 1

chdir = path_of_current_dir

worker_connections = 1000
timeout = 30
max_requests = 2000
graceful_timeout = 30

loglevel = 'info'

reload = True
debug = False

bind = "%s:%s" % ("0.0.0.0", 8000)
pidfile = '/run/adminset.pid'
#errorlog = '%s/logs/adminset_error.log' % (path_of_current_dir)
#accesslog = '%s/logs/adminset_access.log' % (path_of_current_dir)