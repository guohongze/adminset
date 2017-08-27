#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from appconf.models import Project
# Create your models here.
DEPLOY_POLICY = (
    ("Direct", "Direct"),
    ("BlueGreen", "BlueGreen"),
)


class Delivery(models.Model):
    job_name = models.ForeignKey(Project, null=False, verbose_name=u"项目名")
    description = models.CharField(max_length=255, verbose_name=u"描述", null=True, blank=True)
    deploy_policy = models.CharField(max_length=255, choices=DEPLOY_POLICY, verbose_name=u"部署策略")
    shell = models.CharField(max_length=255, verbose_name=u"shell", blank=True)

    def __unicode__(self):
        return self.job_name
