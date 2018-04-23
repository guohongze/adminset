#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:lvhaidong
# datetime:2018/4/19 00:00
# software: PyCharm

import time

import logging
from lib.log import log
from config.views import get_dir

level = get_dir("log_level")
log_path = get_dir("log_path")
log("middleware.log", level, "/Users/lvhaidong/Desktop/main/logs")


class AccessMiddleware(object):
    def process_request(self, request):
        meta = request.META
        print "[%s] PATH_INFO=%s, REMOTE_ADDR=%s, HTTP_USER_AGENT=%s" \
              % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                 meta['PATH_INFO'], meta['REMOTE_ADDR'], meta['HTTP_USER_AGENT'])
        logging.debug("[%s] PATH_INFO=%s, REMOTE_ADDR=%s, HTTP_USER_AGENT=%s" \
                     % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        meta['PATH_INFO'], meta['REMOTE_ADDR'], meta['HTTP_USER_AGENT']))
        logging.info("[%s] PATH_INFO=%s, REMOTE_ADDR=%s, HTTP_USER_AGENT=%s" \
                      % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                         meta['PATH_INFO'], meta['REMOTE_ADDR'], meta['HTTP_USER_AGENT']))
        logging.warning("[%s] PATH_INFO=%s, REMOTE_ADDR=%s, HTTP_USER_AGENT=%s" \
                      % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                         meta['PATH_INFO'], meta['REMOTE_ADDR'], meta['HTTP_USER_AGENT']))
        return None

    def process_response(self, request, response):
        return response
