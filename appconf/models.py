#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from cmdb.models import Host


class AppOwner(models.Model):
    name = models.CharField(u"负责人姓名", max_length=50, unique=True, null=False, blank=False)
    phone = models.CharField(u"负责人手机", max_length=30)
    qq = models.CharField(u"负责人QQ", max_length=100)
    weChat = models.CharField(u"负责人微信", max_length=100)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(u"产品线名称", max_length=50, unique=True, null=False, blank=False)
    description = models.CharField(u"产品线描述", max_length=255)
    owner = models.ForeignKey(
        AppOwner, verbose_name=u"产品线负责人"
    )

    def __unicode__(self):
        return self.name


class Project(models.Model):
    APP_TYPES = (
        ("Tomcat", "Tomcat"),
        ("Php", "Php"),
    )
    name = models.CharField(u"项目名称", max_length=50, unique=True, null=False, blank=False)
    description = models.CharField(u"项目描述", max_length=255)
    type = models.CharField(u"程序类型", choices=APP_TYPES, max_length=30, null=False, blank=False)
    appPath = models.CharField(u"程序路径", max_length=255, null=False, blank=False)
    configPath = models.CharField(u"配置文件路径", max_length=255)
    product = models.ForeignKey(
            Product,
            null=False,
            verbose_name=u"所属产品线"
    )
    owner = models.ForeignKey(
            AppOwner,
            null=False,
            verbose_name=u"项目负责人"
    )
    serverList = models.ManyToManyField(
            Host,
            blank=True,
            verbose_name=u"服务器"
    )






