#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from branches.models import Branch
from branches.forms import BranchForm
from accounts.permission import permission_verify
import csv
import datetime
from cmdb.api import str2gb


@login_required()
@permission_verify()
def branch_list(request):
    all_branch = Branch.objects.all()
    results = {
        'all_branch':  all_branch,
    }
    return render(request, 'branches/branch_list.html', results)


@login_required
@permission_verify()
def branch_del(request):
    branch_id = request.GET.get('id', '')
    if branch_id:
        Branch.objects.filter(id=branch_id).delete()

    branch_id_all = str(request.POST.get('branch_id_all', ''))
    if branch_id_all:
        for branch_id in branch_id_all.split(','):
            Branch.objects.filter(id=branch_id).delete()

    return HttpResponseRedirect(reverse('branch_list'))


@login_required
@permission_verify()
def branch_add(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('branch_list'))
    else:
        form = BranchForm()

    results = {
        'form': form,
        'request': request,
    }
    return render(request, 'branches/branch_base.html', results)


@login_required
@permission_verify()
def branch_edit(request, branch_id):
    branch_obj = Branch.objects.get(id=branch_id)
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch_obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('branch_list'))
    else:
        form = BranchForm(instance=branch_obj)

    results = {
        'form': form,
        'branch_id': branch_id,
        'request': request,
    }
    return render(request, 'branches/branch_base.html', results)


@login_required
@permission_verify()
def branch_export(request):
    export = request.GET.get("export", '')
    branch_id_list = request.GET.getlist("id", '')
    if export == "part":
        if branch_id_list:
            branch_find = []
            for branch_id in branch_id_list:
                branch_item = Branch.objects.get(id=branch_id)
                if branch_item:
                    branch_find.append(branch_item)

    if export == "all":
        branch_find = Branch.objects.all()

    response = HttpResponse(content_type='text/csv')
    now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
    file_name = 'adminset_branch_' + now + '.csv'
    response['Content-Disposition'] = "attachment; filename="+file_name
    writer = csv.writer(response)
    writer.writerow([str2gb(u'机构名称'), str2gb(u'机构地址'), str2gb(u'负责人'), str2gb(u'电话'),
                     str2gb(u'说明'),])
    for p in branch_find:
        writer.writerow([str2gb(p.name), str2gb(p.address), p.owner, p.telphone,
                         str2gb(p.owner)])
    return response


@login_required
@permission_verify()
def resource_detail(request, branch_id):
    branch = Branch.objects.get(id=branch_id)
    resources = branch.resource_set.all()
    results = {
        'resources':  resources,
    }
    return render(request, 'branches/branch_resource_list.html', results)