#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .models import navi
from django.shortcuts import render
from forms import navi_form
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify


@login_required()
@permission_verify()
def index(request):
    temp_name = "navi/navi-header.html"
    allnavi = navi.objects.all()
    return render(request, "navi/index.html", locals())


@login_required()
@permission_verify()
def add(request):
    temp_name = "navi/navi-header.html"
    if request.method == "POST":
        n_form = navi_form(request.POST)
        if n_form.is_valid():
            n_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "navi/add.html", locals())
    else:
        display_control = "none"
        n_form = navi_form()
        return render(request, "navi/add.html", locals())


@login_required()
@permission_verify()
def delete(request):
    temp_name = "navi/navi-header.html"
    if request.method == 'POST':
        navi_items = request.POST.getlist('navi_check', [])
        if navi_items:
            for n in navi_items:
                navi.objects.filter(id=n).delete()
    allnavi = navi.objects.all()
    return render(request, "navi/manage.html", locals())


@login_required()
@permission_verify()
def manage(request):
    temp_name = "navi/navi-header.html"
    allnavi = navi.objects.all()
    return render(request, "navi/manage.html", locals())


@login_required()
@permission_verify()
def edit(request):
    temp_name = "navi/navi-header.html"
    if request.method == 'GET':
        item = request.GET.get("id")
        obj = navi.objects.get(id=item)
    return render(request, "navi/edit.html", locals())


@login_required()
@permission_verify()
def save(request):
    temp_name = "navi/navi-header.html"
    if request.method == 'POST':
        ids = request.POST.get('id')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        url = request.POST.get('url')
        navi_item = navi.objects.get(id=ids)
        navi_item.name = name
        navi_item.description = desc
        navi_item.url = url
        navi_item.save()
        status = 1
    else:
        status = 2
    allnavi = navi.objects.all()
    return render(request, "navi/edit.html", locals())
