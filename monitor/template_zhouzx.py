#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse
from api import GetSysData
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from cmdb.models import Host
import time


@login_required()
@permission_verify()
def index(request):
    temp_name = "monitor/monitor-header.html"
    return render(request, "monitor/template_zhouzx.html", locals())


