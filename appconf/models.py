#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class AuthInfo(models.Model):
    dis_name = models.CharField(u"认证标识", max_length=50, unique=True, blank=False)
    username = models.CharField(u"用户名", max_length=50, blank=True)
    password = models.CharField(u"密码", max_length=50, blank=True)
    deploy_port = models.IntegerField(u"端口", default=22)
    private_key = models.CharField(u"密钥", max_length=2048, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, blank=True)

    def __unicode__(self):
        return self.dis_name


class AppOwner(models.Model):
    name = models.CharField(u"负责人姓名", max_length=50, unique=True, null=False, blank=False)
    phone = models.CharField(u"负责人手机", max_length=50, null=False, blank=False)
    qq = models.CharField(u"负责人QQ", max_length=100, null=True, blank=True)
    weChat = models.CharField(u"负责人微信", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(u"产品线名称", max_length=50, unique=True, null=False, blank=False)
    description = models.CharField(u"产品线描述", max_length=255, null=True, blank=True)
    owner = models.ForeignKey(
        AppOwner, verbose_name=u"产品线负责人",
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return self.name


class Project(models.Model):
    LANGUAGE_TYPES = (
        ("Java", "Java"),
        ("PHP", "PHP"),
        ("Python", "Python"),
        ("C#", "C#"),
        ("Html", "Html"),
        ("Javascript", "Javascript"),
        ("C/C++", "C/C++"),
        ("Ruby", "Ruby"),
        ("Other", "Other"),
    )

    APP_TYPE = (
        ("Frontend", "Frontend"),
        ("Middleware", "Middleware"),
        ("Backend", "Backend"),
    )

    SERVER_TYPE = (
        ("Tomcat", "Tomcat"),
        ("Weblogic", "Weblogic"),
        ("JETTY", "JETTY"),
        ("Nginx", "Nginx"),
        ("Gunicorn", "Gunicorn"),
        ("Uwsgi", "Uwsgi"),
        ("Apache", "Apache"),
        ("IIS", "IIS"),
    )

    APP_ARCH = (
        ("Django", "Django"),
        ("Flask", "Flask"),
        ("Tornado", "Tornado"),
        ("Dubbo", "Dubbo"),
        ("SSH", "SSH"),
        ("Spring boot", "Spring boot"),
        ("Spring cloud", "Spring cloud"),
        ("Laravel", "Laravel"),
        ("ThinkPHP", "ThinkPHP"),
        ("Phalcon", "Phalcon"),
        ("other", "other"),
    )

    SOURCE_TYPE = (
        ("git", "git"),
        ("svn", "svn"),
    )

    name = models.CharField(u"项目名称", max_length=50, unique=True, null=False, blank=False)
    description = models.CharField(u"项目描述", max_length=255, null=True, blank=True)
    language_type = models.CharField(u"语言类型", choices=LANGUAGE_TYPES, max_length=30, null=True, blank=True)
    app_type = models.CharField(u"程序类型", choices=APP_TYPE, max_length=30, null=True, blank=True)
    server_type = models.CharField(u"服务器类型", choices=SERVER_TYPE, max_length=30, null=True, blank=True)
    app_arch = models.CharField(u"程序框架", choices=APP_ARCH, max_length=30, null=True, blank=True)
    source_type = models.CharField(max_length=255, choices=SOURCE_TYPE, verbose_name=u"源类型", blank=True)
    source_address = models.CharField(max_length=255, verbose_name=u"源地址", null=True, blank=True)
    appPath = models.CharField(u"程序部署路径", max_length=255, null=True, blank=True)
    configPath = models.CharField(u"配置文件路径", max_length=255, null=True, blank=True)
    product = models.ForeignKey(
            Product,
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            verbose_name=u"所属产品线"
    )
    owner = models.ForeignKey(
            AppOwner,
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            verbose_name=u"项目负责人"
    )

    def __unicode__(self):
        return self.name




