#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from models import HostGroup
from forms import GroupForm
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


@login_required()
@permission_verify()
def group(request):
    temp_name = "cmdb/cmdb-header.html"
    allgroup = HostGroup.objects.all()
    context = {
        'temp_name': temp_name,
        'allgroup': allgroup
    }
    return render(request, 'cmdb/group.html', context)


@login_required()
@permission_verify()
def group_add(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == "POST":
        group_form = GroupForm(request.POST)
        if group_form.is_valid():
            group_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "cmdb/group_base.html", locals())
    else:
        display_control = "none"
        group_form = GroupForm()
        return render(request, "cmdb/group_base.html", locals())


@login_required()
@permission_verify()
def group_del(request):
    temp_name = "cmdb/cmdb-header.html"

    group_id = request.GET.get('id', '')
    if group_id:
        HostGroup.objects.filter(id=group_id).delete()

    if request.method == 'POST':
        group_items = request.POST.getlist('g_check', [])
        if group_items:
            for n in group_items:
                HostGroup.objects.filter(id=n).delete()
    allgroup = HostGroup.objects.all()
    return render(request, "cmdb/group.html", locals())


@login_required()
@permission_verify()
def group_edit(request, group_id):
    project = HostGroup.objects.get(id=group_id)
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('group'))
    else:
        form = GroupForm(instance=project)
    display_control = "none"
    results = {
        'group_form': form,
        'group_id': group_id,
        'request': request,
        'temp_name': temp_name,
        'display_control': display_control,
    }
    return render(request, 'cmdb/group_base.html', results)


@login_required
@permission_verify()
def server_list(request, group_id):
    temp_name = "cmdb/cmdb-header.html"
    grp = HostGroup.objects.get(id=group_id)
    servers = grp.serverList.all()
    results = {
        'temp_name': temp_name,
        'server_list':  servers,
    }
    return render(request, 'cmdb/group_server_list.html', results)