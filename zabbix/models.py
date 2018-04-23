#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:lvhaidong
# datetime:2018/4/21 23:57
# software: PyCharm

from __future__ import unicode_literals

from django.db import models


class Host(models.Model):
    ip = models.GenericIPAddressField(u"IP", max_length=30)

    def __unicode__(self):
        return self.ip
