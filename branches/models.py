# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from appconf.models import AppOwner
# Create your models here.


class Branch(models.Model):
    name = models.CharField(max_length=255, verbose_name="分支机构", blank=False, unique=True, null=False)
    address = models.CharField(max_length=255, verbose_name="办公地址", blank=True, null=True)
    telphone = models.IntegerField(verbose_name="联系电话", blank=True, null=True)
    description = models.CharField(max_length=255, verbose_name="备注", blank=True, null=True)
    owner = models.ForeignKey(
        AppOwner,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=u"负责人"
    )

    def __unicode__(self):
        return self.name


class SubBranch(models.Model):
    name = models.CharField(max_length=255, verbose_name="分支机构", blank=False, unique=True, null=False)
    address = models.CharField(max_length=255, verbose_name="办公地址", blank=True, null=True)
    telphone = models.IntegerField(verbose_name="联系电话", blank=True, null=True)
    description = models.CharField(max_length=255, verbose_name="备注", blank=True, null=True)
    owner = models.ForeignKey(
        AppOwner,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=u"负责人"
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=u"所属分支"
    )

    def __unicode__(self):
        return self.name


class Resource(models.Model):
    name = models.CharField(max_length=255, verbose_name="资源名", blank=False, null=False)
    budget = models.IntegerField(verbose_name="预算", blank=True, null=True)
    paid = models.IntegerField(verbose_name="合同金额", blank=True, null=True)
    contract = models.CharField(max_length=255, verbose_name="合同编号", blank=True, null=True)
    contract_start = models.DateField(max_length=255, verbose_name="合同开始", blank=True, null=True)
    contract_end = models.DateField(verbose_name="合同结束", blank=True, null=True)
    description = models.CharField(max_length=255, verbose_name="合同说明", blank=True, null=True)
    supplier = models.CharField(max_length=255, verbose_name="合同说明", blank=True, null=True)
    service_phone = models.IntegerField(verbose_name="服务电话", blank=True, null=True)
    subBranch = models.ForeignKey(
        SubBranch,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=u"所属中心"
    )

    def __unicode__(self):
        return self.name
