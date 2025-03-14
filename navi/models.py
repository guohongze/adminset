#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


class navi(models.Model):
    name = models.CharField("名称", max_length=50)
    description = models.CharField("描述", max_length=50)
    url = models.URLField("网址")

    def __str__(self):
        return self.name
