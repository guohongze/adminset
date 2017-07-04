#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from models import Host, HostGroup
from forms import GroupForm, IdcForm
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify


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
        return render(request, "cmdb/group_add.html", locals())
    else:
        display_control = "none"
        group_form = GroupForm()
        idc_form = IdcForm()
        return render(request, "cmdb/group_add.html", locals())


@login_required()
@permission_verify()
def group_del(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'POST':
        group_items = request.POST.getlist('g_check', [])
        if group_items:
            for n in group_items:
                HostGroup.objects.filter(id=n).delete()
    allgroup = HostGroup.objects.all()
    return render(request, "cmdb/group.html", locals())


@login_required()
@permission_verify()
def group_edit(request, ids):
    obj = HostGroup.objects.get(id=ids)
    allgroup = HostGroup.objects.all()
    unselect = Host.objects.filter(group__name=None)
    members = Host.objects.filter(group__name=obj.name)
    return render(request, "cmdb/group_edit.html", locals())


@login_required()
@permission_verify()
def group_save(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'POST':
        group_id = request.POST.get('id')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        members = request.POST.getlist('members', [])
        unselect = request.POST.getlist('unselect', [])
        group_item = HostGroup.objects.get(id=group_id)
        if unselect:
            for host in unselect:
                # print "unselect: "+host
                obj = Host.objects.get(hostname=host)
                obj.group_id = None
                obj.save()
        if members:
            for host in members:
                # print "members: "+host
                obj = Host.objects.get(hostname=host)
                obj.group_id = group_id
                obj.save()
        group_item.name = name
        group_item.desc = desc
        group_item.save()
        obj = group_item
        status = 1
    else:
        status = 2
    return render(request, "cmdb/group_edit.html", locals())
