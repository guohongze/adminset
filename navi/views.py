#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import navi
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from forms import navi_form

def index(request):
    temp_name = "navi/navi-header.html"
    allnavi = navi.objects.all()
    return render_to_response("navi/index.html",locals())


def add(request):
    temp_name = "navi/navi-header.html"
    if request.method == "POST":
        n_form = navi_form(request.POST)
        if n_form.is_valid():
            n_form.save()
            tips = u"增加成功！"
        return render_to_response("navi/add.html", locals())
    else:
        n_form = navi_form()
        return render_to_response("navi/add.html", locals())

def delete(request):
    pass


def manage(request):
    temp_name = "navi/navi-header.html"
    allnavi = navi.objects.all()
    return render_to_response("navi/manage.html", locals())