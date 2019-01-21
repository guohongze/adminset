#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from branches.models import Region
from branches.forms import RegionForm
from accounts.permission import permission_verify


@login_required()
@permission_verify()
def region_list(request):
    regions = Region.objects.all()
    results = {
        'regions':  regions,
    }
    return render(request, 'branches/region_list.html', results)


@login_required
@permission_verify()
def region_del(request):
    region_id = request.GET.get('id', '')
    if region_id:
        Region.objects.filter(id=region_id).delete()

    region_id_all = str(request.POST.get('region_id_all', ''))
    if region_id_all:
        for region_id in region_id_all.split(','):
            Region.objects.filter(id=region_id).delete()

    return HttpResponseRedirect(reverse('region_list'))


@login_required
@permission_verify()
def region_add(request):
    if request.method == 'POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('region_list'))
    else:
        form = RegionForm()

    results = {
        'form': form,
        'request': request,
    }
    return render(request, 'branches/region_base.html', results)


@login_required
@permission_verify()
def region_edit(request, region_id):
    region_obj = get_object_or_404(Region, pk=region_id)
    if request.method == 'POST':
        form = RegionForm(request.POST, instance=region_obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('region_list'))
    else:
        form = RegionForm(instance=region_obj)

    results = {
        'form': form,
        'region_id': region_id,
        'request': request,
    }
    return render(request, 'branches/region_base.html', results)


@login_required
@permission_verify()
def branch_detail(request, region_id):
    region = Region.objects.get(id=region_id)
    branches = region.branch_set.all()
    results = {
        'branches':  branches,
    }
    return render(request, 'branches/region_branch_list.html', results)



