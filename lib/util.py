#!/bin/env python
# -*- encoding: utf-8 -*-

import os, os.path
import time, json
import base64, glob
import hashlib
import ConfigParser
import logging, logging.config


def get_config(service_conf, section='db'):
    config = ConfigParser.ConfigParser()
    config.read(service_conf)
    conf_items = dict(config.items(section)) if config.has_section(section) else {}
    return conf_items


def check_name(name):
    if isinstance(name, str) or isinstance(name, unicode):
        return name.isalnum() and len(name) >= 2
    else:
        return False


def graph_file(name):
    try:
        file = glob.glob(name + '/*')
        for i in file:
            os.remove(i)
    except:
        return 1


def graph_img(name):
    try:
        ret = []
        file = glob.glob(name + '/*')
        for i in file:
            ret.append(i.split("static")[1])
        return ret
    except:
        return ret
