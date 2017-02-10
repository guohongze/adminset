#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,redirect
from navi.models import navi


def index(request):
    allnavi = navi.objects.all()
    return render_to_response("index.html",locals())