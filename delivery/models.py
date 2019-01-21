#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from appconf.models import Project, AuthInfo
from cmdb.models import Host

# Create your models here.
DEPLOY_POLICY = (
    ("Direct", "Direct"),
    # ("BlueGreen", "BlueGreen"),
)


class Delivery(models.Model):
    job_name = models.OneToOneField(Project, verbose_name=u"项目名")
    description = models.CharField(max_length=255, verbose_name=u"项目描述", null=True, blank=True)
    deploy_policy = models.CharField(max_length=255, choices=DEPLOY_POLICY, verbose_name=u"部署策略")
    version = models.CharField(max_length=255, verbose_name=u"版本信息", blank=True)
    build_clean = models.BooleanField(verbose_name=u"清理构建", default=False)
    rsync_delete = models.BooleanField(verbose_name=u"同步删除", default=True)
    shell = models.CharField(max_length=2048, verbose_name=u"shell", blank=True)
    shell_position = models.BooleanField(verbose_name=u"本地执行", default=False)
    status = models.BooleanField(verbose_name=u"部署状态", default=False)
    deploy_num = models.IntegerField(verbose_name=u"部署次数", default=0)
    bar_data = models.IntegerField(default=0)
    source_auth = models.BooleanField(verbose_name=u"源码认证", default=False)
    auth = models.ForeignKey(
        AuthInfo, verbose_name=u"认证信息",
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    serverList = models.ManyToManyField(
            Host,
            blank=True,
            verbose_name=u"所在服务器"
    )

    def __unicode__(self):
        return self.job_name
