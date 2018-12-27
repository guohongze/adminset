# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from appconf.models import AppOwner
# Create your models here.


class Region(models.Model):
    name = models.CharField(max_length=255, verbose_name="行政区域", blank=False, unique=True, null=False)
    address = models.CharField(max_length=255, verbose_name="办公地址", blank=True, null=True)
    telephone = models.CharField(max_length=25, verbose_name="联系电话", blank=True, null=True)
    owner = models.ForeignKey(
        AppOwner,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=u"负责人"
    )
    description = models.CharField(max_length=255, verbose_name="备注信息", blank=True, null=True)

    def __unicode__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=255, verbose_name="分支机构", blank=False, unique=True, null=False)
    address = models.CharField(max_length=255, verbose_name="办公地址", blank=True, null=True)
    telephone = models.CharField(max_length=25, verbose_name="联系电话", blank=True, null=True)
    owner = models.ForeignKey(
        AppOwner,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=u"负责人"
    )
    region = models.ForeignKey(
        Region,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=u"所属大区"
    )
    description = models.CharField(max_length=255, verbose_name="备注", blank=True, null=True)

    def __unicode__(self):
        return self.name


class Resource(models.Model):
    sn = models.CharField(max_length=255, verbose_name="资源编码", blank=False, null=False)
    name = models.CharField(max_length=255, verbose_name="资源名称", blank=False, null=False)
    spec = models.CharField(max_length=255, verbose_name="资源规格", blank=False, null=False)
    budget = models.CharField(max_length=255, verbose_name="预算金额", blank=True, null=True)
    paid = models.CharField(max_length=255, verbose_name="合同金额", blank=True, null=True)
    contract = models.CharField(max_length=255, verbose_name="合同编号", blank=True, null=True)
    contract_start = models.DateField(max_length=255, verbose_name="合同开始", blank=True, null=True)
    contract_end = models.DateField(verbose_name="合同结束", blank=True, null=True)
    supplier = models.CharField(max_length=255, verbose_name="供应商名", blank=True, null=True)
    service_phone = models.CharField(max_length=25, verbose_name="服务电话", blank=True, null=True)
    branch = models.ForeignKey(
        Branch,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=u"所属机构"
    )
    owner = models.ForeignKey(
        AppOwner,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=u"供应商联系人"
    )
    description = models.CharField(max_length=255, verbose_name="合同说明", blank=True, null=True)

    def __unicode__(self):
        return self.name
