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
from cmdb.api import str2gb


@login_required()
@permission_verify()
def resource_list(request):
    temp_name = "branches/header.html"
    resources = Resource.objects.all()
    results = {
        'temp_name': temp_name,
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
    temp_name = "branches/header.html"
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
        'temp_name': temp_name,
    }
    return render(request, 'branches/resource_base.html', results)


@login_required
@permission_verify()
def resource_edit(request, resource_id):
    resource_obj = Resource.objects.get(id=resource_id)
    temp_name = "branches/header.html"
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
        'temp_name': temp_name,
    }
    return render(request, 'branches/resource_base.html', results)


@login_required
@permission_verify()
def resource_export(request):
    export = request.GET.get("export", '')
    resource_id_list = request.GET.getlist("id", '')
    if export == "part":
        if resource_id_list:
            resource_find = []
            for resource_id in resource_id_list:
                resource_item = Resource.objects.get(id=resource_id)
                if resource_item:
                    resource_find.append(resource_item)

    if export == "all":
        resource_find = Resource.objects.all()

    response = HttpResponse(content_type='text/csv')
    now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
    file_name = 'adminset_resource_' + now + '.csv'
    response['Content-Disposition'] = "attachment; filename="+file_name
    writer = csv.writer(response)
    writer.writerow([str2gb(u'资源名称'), str2gb(u'资源规格'), str2gb(u'预算金额'), str2gb(u'合同金额'),
                     str2gb(u'合同编号'), str2gb(u'合同开始'), str2gb(u'合同结束'), str2gb(u'供应商名'),
                     str2gb(u'服务电话'), str2gb(u'所属机构'), str2gb(u'备注说明')])
    for p in resource_find:
        writer.writerow([str2gb(p.name), str2gb(p.spec), str2gb(p.budget), str2gb(p.paid), str2gb(p.contract),
                         str2gb(p.contract_start),str2gb(p.contract_end), str2gb(p.suppier), str2gb(p.service_phone),
                         str2gb(p.branch), str2gb(p.description)])
    return response


@login_required
@permission_verify()
def resource_export(request):
    resource = Resource.objects.all()
    response = HttpResponse(content_type='text/csv')
    now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
    file_name = 'adminset_resource_' + now + '.csv'
    response['Content-Disposition'] = "attachment; filename=" + file_name
    writer = csv.writer(response)
    writer.writerow([str2gb('行政区域'), str2gb('分支机构'), str2gb('资源编码'), str2gb('资源名称'), str2gb('资源规格'),
                     str2gb('预算资金'), str2gb('合同资金'), str2gb('合同编号'), str2gb('合同开始'), str2gb('合同结束'),
                     str2gb('供应商名'), str2gb('服务电话'), str2gb('客户经理'), str2gb('联系电话'),
                     str2gb('备注说明')])
    for r in resource:
        if r.branch:
            br = Branch.objects.get(name=r.branch)
        else:
            br = ""
        writer.writerow([str2gb(br.region.name), str2gb(r.branch.name), r.sn, str2gb(r.name), str2gb(r.spec),
                         str2gb(r.budget), str2gb(r.paid), str2gb(r.contract), str2gb(r.contract_start), str2gb(r.contract_end),
                         str2gb(r.supplier), str2gb(r.service_phone), str2gb(r.owner), str2gb(r.owner.phone),
                         str2gb(r.description)])
    return response
