#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class UserInfo(models.Model):
    username = models.CharField(max_length=30,null=True)
    password = models.CharField(max_length=30,null=True)

    def __unicode__(self):
        return self.username


class Idc(models.Model):
    name = models.CharField(max_length=30,null=True)
    address = models.CharField(max_length=100,null=True)
    tel = models.CharField(max_length=30,null=True)
    contact = models.CharField(max_length=30,null=True)

    def __unicode__(self):
        return self.name


class Host(models.Model):
    hostname = models.CharField(max_length=30, verbose_name=u"主机名")
    os = models.CharField(max_length=50,null=True)
    vendor = models.CharField(max_length=30,null=True)
    group = models.CharField(max_length=30,null=True)
    cpu_model = models.CharField(max_length=100,null=True)
    cpu_num = models.IntegerField(null=True)
    memory = models.IntegerField(null=True)
    disk = models.CharField(max_length=255,null=True)
    sn = models.CharField(max_length=60)
    ip = models.GenericIPAddressField(max_length=15)
    identity = models.CharField(max_length=32,null=True)
    idc = models.ForeignKey(Idc, verbose_name=u"所在机房",null=True)

    def __unicode__(self):
        return self.hostname


class HostGroup(models.Model):
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(Host)

    def __unicode__(self):
        return self.name


class IpSource(models.Model):
    net = models.CharField(max_length=30)
    subnet = models.CharField(max_length=30,null=True)
    describe = models.CharField(max_length=30,null=True)

    def __unicode__(self):
        return self.net


class InterFace(models.Model):
    name = models.CharField(max_length=30)
    vendor = models.CharField(max_length=30,null=True)
    bandwidth = models.CharField(max_length=30,null=True)
    tel = models.CharField(max_length=30,null=True)
    contact = models.CharField(max_length=30,null=True)
    startdate = models.DateField()
    enddate = models.DateField()
    price = models.IntegerField(verbose_name=u'价格')

    def __unicode__(self):
        return self.name
