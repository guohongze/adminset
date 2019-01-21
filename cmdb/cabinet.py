#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from cmdb.models import Cabinet
from cmdb.forms import CabinetForm
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


@login_required()
@permission_verify()
def cabinet(request):
    allcabinet = Cabinet.objects.all()
    context = {
        'allcabinet': allcabinet
    }
    return render(request, 'cmdb/cabinet.html', context)


@login_required()
@permission_verify()
def cabinet_add(request):
    if request.method == "POST":
        cabinet_form = CabinetForm(request.POST)
        if cabinet_form.is_valid():
            cabinet_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "cmdb/cabinet_base.html", locals())
    else:
        display_control = "none"
        cabinet_form = CabinetForm()
        return render(request, "cmdb/cabinet_base.html", locals())


@login_required()
@permission_verify()
def cabinet_del(request):
    cabinet_id = request.GET.get('id', '')
    if cabinet_id:
        Cabinet.objects.filter(id=cabinet_id).delete()

    if request.method == 'POST':
        cabinet_items = request.POST.getlist('g_check', [])
        if cabinet_items:
            for n in cabinet_items:
                Cabinet.objects.filter(id=n).delete()
    allcabinet = Cabinet.objects.all()
    return render(request, "cmdb/cabinet.html", locals())


@login_required()
@permission_verify()
def cabinet_edit(request, cabinet_id):
    project = Cabinet.objects.get(id=cabinet_id)
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'POST':
        form = CabinetForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cabinet'))
    else:
        form = CabinetForm(instance=project)
    display_control = "none"
    results = {
        'cabinet_form': form,
        'cabinet_id': cabinet_id,
        'request': request,
        'temp_name': temp_name,
        'display_control': display_control,
    }
    return render(request, 'cmdb/cabinet_base.html', results)


@login_required
@permission_verify()
def server_list(request, cabinet_id):
    cab = Cabinet.objects.get(id=cabinet_id)
    servers = cab.serverList.all()
    results = {
        'server_list':  servers,
    }
    return render(request, 'cmdb/cabinet_server_list.html', results)