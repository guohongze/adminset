#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from adminset.settings import BASE_DIR


def log(log_name):
    logging.basicConfig(level=logging.INFO,
                # format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%Y%m%d %H:%M:%S',
                filename=BASE_DIR+'/logs/'+log_name,
                filemode='ab+')
    return logging.basicConfig
