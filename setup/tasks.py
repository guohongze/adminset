#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def add(x, y):
    print "test!!!!"
    return x + y


@shared_task
def plus(x, y):
    print "test!!!!"
    return x * y
