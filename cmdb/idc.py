#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from cmdb.forms import IdcForm
from .models import Idc, Cabinet
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


@login_required()
@permission_verify()
def idc(request):
    temp_name = "cmdb/cmdb-header.html"
    idc_info = Idc.objects.all()
    return render(request, 'cmdb/idc.html', locals())


@login_required()
@permission_verify()
def idc_add(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == "POST":
        idc_form = IdcForm(request.POST)
        if idc_form.is_valid():
            idc_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "cmdb/idc_base.html", locals())
    else:
        display_control = "none"
        idc_form = IdcForm()
        return render(request, "cmdb/idc_base.html", locals())


@login_required()
@permission_verify()
def idc_del(request):
    temp_name = "cmdb/cmdb-header.html"
    idc_id = request.GET.get('id', '')
    if idc_id:
        Idc.objects.filter(id=idc_id).delete()
    if request.method == 'POST':
        idc_items = request.POST.getlist('idc_check', [])
        if idc_items:
            for n in idc_items:
                Idc.objects.filter(id=n).delete()
    idc_info = Idc.objects.all()
    return render(request, "cmdb/idc.html", locals())


@login_required()
@permission_verify()
def idc_edit(request, idc_id):
    project = Idc.objects.get(id=idc_id)
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'POST':
        form = IdcForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('idc'))
    else:
        form = IdcForm(instance=project)
    display_control = "none"
    results = {
        'idc_form': form,
        'idc_id': idc_id,
        'request': request,
        'temp_name': temp_name,
        'display_control': display_control,
    }
    return render(request, 'cmdb/idc_base.html', results)


@login_required
@permission_verify()
def cabinet_list(request, idc_id):
    temp_name = "cmdb/cmdb-header.html"
    cab = Idc.objects.get(id=idc_id)
    cabinets = cab.cabinet_set.all()
    results = {
        'temp_name': temp_name,
        'cabinet_list':  cabinets,
    }
    return render(request, 'cmdb/idc_cabinet_list.html', results)