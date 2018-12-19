#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from branches.models import Branch
from branches.forms import BranchForm
from accounts.permission import permission_verify


@login_required()
@permission_verify()
def branch_list(request):
    temp_name = "branches/branch_header.html"
    all_branch = Branch.objects.all()
    results = {
        'temp_name': temp_name,
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
    temp_name = "branches/branch_header.html"
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
        'temp_name': temp_name,
    }
    return render(request, 'branches/branch_base.html', results)


@login_required
@permission_verify()
def branch_edit(request, branch_id):
    branch_obj = get_object_or_404(Branch, pk=branch_id)
    temp_name = "branches/branch_header.html"
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
        'temp_name': temp_name,
    }
    return render(request, 'branches/branch_base.html', results)


@login_required
@permission_verify()
def project_list(request, branch_id):
    pass
    # temp_name = "appconf/appconf-header.html"
    # product = Product.objects.get(id=product_id)
    # projects = product.project_set.all()
    # results = {
    #     'temp_name': temp_name,
    #     'project_list':  projects,
    # }
    # return render(request, 'appconf/product_project_list.html', results)



