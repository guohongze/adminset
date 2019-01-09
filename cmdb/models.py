#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from appconf.models import AuthInfo

ASSET_STATUS = (
    (str(1), u"使用中"),
    (str(2), u"未使用"),
    (str(3), u"故障"),
    (str(4), u"其它"),
    )

ASSET_TYPE = (
    (str(1), u"物理机"),
    (str(2), u"虚拟机"),
    (str(3), u"容器"),
    (str(4), u"网络设备"),
    (str(5), u"安全设备"),
    (str(6), u"其他")
    )


class UserInfo(models.Model):
    username = models.CharField(max_length=30,null=True)
    password = models.CharField(max_length=30,null=True)

    def __unicode__(self):
        return self.username


class Idc(models.Model):
    ids = models.CharField(u"机房标识", max_length=255, unique=True)
    name = models.CharField(u"机房名称", max_length=255, unique=True)
    address = models.CharField(u"机房地址", max_length=100, blank=True)
    tel = models.CharField(u"机房电话", max_length=30, blank=True)
    contact = models.CharField(u"客户经理", max_length=30, blank=True)
    contact_phone = models.CharField(u"移动电话", max_length=30, blank=True)
    jigui = models.CharField(u"机柜信息", max_length=30, blank=True)
    ip_range = models.CharField(u"IP范围", max_length=30, blank=True)
    bandwidth = models.CharField(u"接入带宽", max_length=30, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'数据中心'
        verbose_name_plural = verbose_name


class Host(models.Model):
    hostname = models.CharField(max_length=50, verbose_name=u"主机名", unique=True)
    ip = models.GenericIPAddressField(u"管理IP", max_length=15)
    account = models.ForeignKey(AuthInfo, verbose_name=u"账号信息", on_delete=models.SET_NULL, null=True, blank=True)
    idc = models.ForeignKey(Idc, verbose_name=u"所在机房", on_delete=models.SET_NULL, null=True, blank=True)
    other_ip = models.CharField(u"其它IP", max_length=100, blank=True)
    asset_no = models.CharField(u"资产编号", max_length=50, blank=True)
    asset_type = models.CharField(u"设备类型", choices=ASSET_TYPE, max_length=30, null=True, blank=True)
    status = models.CharField(u"设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    os = models.CharField(u"操作系统", max_length=100, blank=True)
    vendor = models.CharField(u"设备厂商", max_length=50, blank=True)
    up_time = models.CharField(u"上架时间", max_length=50, blank=True)
    cpu_model = models.CharField(u"CPU型号", max_length=100, blank=True)
    cpu_num = models.CharField(u"CPU数量", max_length=100, blank=True)
    memory = models.CharField(u"内存大小", max_length=30, blank=True)
    disk = models.CharField(u"硬盘信息", max_length=255, blank=True)
    sn = models.CharField(u"SN号 码", max_length=60, blank=True)
    position = models.CharField(u"所在位置", max_length=100, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, blank=True)

    def __unicode__(self):
        return self.hostname


class Cabinet(models.Model):
    idc = models.ForeignKey(Idc, verbose_name=u"所在机房", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(u"机柜", max_length=100)
    desc = models.CharField(u"描述", max_length=100, blank=True)

    serverList = models.ManyToManyField(
            Host,
            blank=True,
            verbose_name=u"所在服务器"
    )

    def __unicode__(self):
        return self.name


class HostGroup(models.Model):
    name = models.CharField(u"服务器组名", max_length=30, unique=True)
    desc = models.CharField(u"描述", max_length=100, blank=True)

    serverList = models.ManyToManyField(
            Host,
            blank=True,
            verbose_name=u"所在服务器"
    )

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
