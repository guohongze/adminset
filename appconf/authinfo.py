#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import AuthInfo
from .forms import AuthInfoForm
from accounts.permission import permission_verify


@login_required()
@permission_verify()
def authinfo_list(request):
    temp_name = "appconf/appconf-header.html"
    all_authinfo = AuthInfo.objects.all()
    results = {
        'temp_name': temp_name,
        'all_authinfo':  all_authinfo,
    }
    return render(request, 'appconf/authinfo_list.html', results)


@login_required
@permission_verify()
def authinfo_del(request):
    authinfo_id = request.GET.get('id', '')
    if authinfo_id:
        AuthInfo.objects.filter(id=authinfo_id).delete()
    authinfo_id_all = str(request.POST.get('authinfo_id_all', ''))
    if authinfo_id_all:
        for authinfo_id in authinfo_id_all.split(','):
            AuthInfo.objects.filter(id=authinfo_id).delete()
    return HttpResponseRedirect(reverse('authinfo_list'))


@login_required
@permission_verify()
def authinfo_add(request):
    temp_name = "appconf/appconf-header.html"
    if request.method == 'POST':
        form = AuthInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('authinfo_list'))
    else:
        form = AuthInfoForm()

    results = {
        'form': form,
        'request': request,
        'temp_name': temp_name,
        'page_type': "whole"
    }
    return render(request, 'appconf/authinfo_add_edit.html', results)


@login_required
@permission_verify()
def authinfo_add_mini(request):
    status = 0
    authinfo_id = 0
    if request.method == 'POST':
        form =AuthInfoForm(request.POST)
        if form.is_valid():
            form.save()
            auth_name = request.POST.get('username', '')
            auth_info = AuthInfo.objects.get(username=auth_name)
            authinfo_id = auth_info.id
            status = 1
        else:
            status = 2
    else:
        form = AuthInfoForm()

    results = {
        'form': form,
        'request': request,
        'status': status,
        'auth_id': authinfo_id,
        'auth_name': request.POST.get('username', ''),
        'page_type': "mini"
    }
    return render(request, 'appconf/authinfo_add_edit_mini.html', results)


@login_required
@permission_verify()
def authinfo_edit(request, authinfo_id, mini=False):
    authinfo = AuthInfo.objects.get(id=authinfo_id)
    temp_name = "appconf/appconf-header.html"
    if request.method == 'POST':
        form = AuthInfoForm(request.POST, instance=authinfo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('authinfo_list'))
    else:
        form = AuthInfoForm(instance=authinfo)

    results = {
        'form': form,
        'authinfo_id': authinfo_id,
        'request': request,
        'temp_name': temp_name,
        'page_type': "whole"
    }
    return render(request, 'appconf/authinfo_add_edit.html', results)

