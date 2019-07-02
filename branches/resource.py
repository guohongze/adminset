#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from branches.models import Resource, Branch
from branches.forms import ResourceForm
from accounts.permission import permission_verify
import csv
import datetime
from cmdb.api import str2gb, str2gbk


@login_required()
@permission_verify()
def resource_list(request):
    resources = Resource.objects.all()
    results = {
        'resources':  resources,
    }
    return render(request, 'branches/resource_list.html', results)


@login_required
@permission_verify()
def resource_del(request):
    resource_id = request.GET.get('id', '')
    if resource_id:
        Resource.objects.filter(id=resource_id).delete()

    resource_id_all = str(request.POST.get('resource_id_all', ''))
    if resource_id_all:
        for resource_id in resource_id_all.split(','):
            Resource.objects.filter(id=resource_id).delete()

    return HttpResponseRedirect(reverse('resource_list'))


@login_required
@permission_verify()
def resource_add(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('resource_list'))
    else:
        form = ResourceForm()

    results = {
        'form': form,
        'request': request,
    }
    return render(request, 'branches/resource_base.html', results)


@login_required
@permission_verify()
def resource_edit(request, resource_id):
    resource_obj = Resource.objects.get(id=resource_id)
    if request.method == 'POST':
        form = ResourceForm(request.POST, instance=resource_obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('resource_list'))
    else:
        form = ResourceForm(instance=resource_obj)

    results = {
        'form': form,
        'resource_id': resource_id,
        'request': request,
    }
    return render(request, 'branches/resource_base.html', results)

@login_required
@permission_verify()
def resource_export(request):
    resource_find = Resource.objects.all()
    response = HttpResponse(content_type='text/csv')
    now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
    file_name = 'adminset_resource_' + now + '.csv'
    response['Content-Disposition'] = "attachment; filename=" + file_name
    writer = csv.writer(response)
    writer.writerow([str2gb('行政区域'), str2gb('分支机构'), str2gb('资源编码'), str2gb('资源名称'), str2gb('资源规格'),
                     str2gb('预算资金'), str2gb('合同资金'), str2gb('合同编号'), str2gb('合同开始'), str2gb('合同结束'),
                     str2gb('供应商名'), str2gb('服务电话'), str2gb('客户经理'), str2gb('联系电话'),])
    for r in resource_find:
        br_name = ""
        if r.branch:
            br = Branch.objects.get(name=r.branch)
            if br.region:
                br_name = br.region.name
        writer.writerow([str2gb(br_name), str2gbk(r.branch.name if r.branch else None), str2gb(r.sn),
                         str2gb(r.name), str2gb(r.spec), str2gb(r.budget), str2gb(r.paid), str2gb(r.contract),
                         str2gb(r.contract_start), str2gb(r.contract_end),
                         str2gb(r.supplier), r.service_phone, str2gb(r.owner if r.owner else None),
                         str2gb(r.owner.phone if r.owner else None),])
    return response
