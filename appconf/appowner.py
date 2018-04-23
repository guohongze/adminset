#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from models import AppOwner
from forms import AppOwnerForm
from accounts.permission import permission_verify


@login_required()
@permission_verify()
def appowner_list(request):
    temp_name = "appconf/appconf-header.html"
    all_app_owner = AppOwner.objects.all()
    results = {
        'temp_name': temp_name,
        'all_app_owner':  all_app_owner,
    }
    return render(request, 'appconf/appowner_list.html', results)


@login_required
@permission_verify()
def appowner_del(request):
    appowner_id = request.GET.get('id', '')
    if appowner_id:
        AppOwner.objects.filter(id=appowner_id).delete()

    appowner_id_all = str(request.POST.get('appowner_id_all', ''))
    if appowner_id_all:
        for appowner_id in appowner_id_all.split(','):
            AppOwner.objects.filter(id=appowner_id).delete()

    return HttpResponseRedirect(reverse('appowner_list'))


@login_required
@permission_verify()
def appowner_add(request):
    temp_name = "appconf/appconf-header.html"
    if request.method == 'POST':
        form = AppOwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('appowner_list'))
    else:
        form = AppOwnerForm()

    results = {
        'form': form,
        'request': request,
        'temp_name': temp_name,
        'page_type': "whole"
    }
    return render(request, 'appconf/appowner_add_edit.html', results)


@login_required
@permission_verify()
def appowner_add_mini(request):
    status = 0
    owner_id = 0
    if request.method == 'POST':
        form = AppOwnerForm(request.POST)
        if form.is_valid():
            form.save()
            owner_name = request.POST.get('name', '')
            app_owner = AppOwner.objects.get(name=owner_name)
            owner_id = app_owner.id
            status = 1
        else:
            status = 2
    else:
        form = AppOwnerForm()

    results = {
        'form': form,
        'request': request,
        'status': status,
        'owner_id': owner_id,
        'owner_name': request.POST.get('name', ''),
        'page_type': "mini"
    }
    return render(request, 'appconf/appowner_add_edit_mini.html', results)


@login_required
@permission_verify()
def appowner_edit(request, appowner_id, mini=False):
    appowner = AppOwner.objects.get(id=appowner_id)
    temp_name = "appconf/appconf-header.html"
    if request.method == 'POST':
        form = AppOwnerForm(request.POST, instance=appowner)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('appowner_list'))
    else:
        form = AppOwnerForm(instance=appowner)

    results = {
        'form': form,
        'appowner_id': appowner_id,
        'request': request,
        'temp_name': temp_name,
        'page_type': "whole"
    }
    return render(request, 'appconf/appowner_add_edit.html', results)

