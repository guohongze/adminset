#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.forms import RoleListForm
from accounts.models import RoleList
from accounts.permission import permission_verify


@login_required
@permission_verify()
def role_add(request):
    if request.method == "POST":
        form = RoleListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('role_list'))
    else:
        form = RoleListForm()

    kwvars = {
        'form': form,
        'request': request,
    }

    return render(request, 'accounts/role_add.html', kwvars)


@login_required
@permission_verify()
def role_list(request):
    all_role = RoleList.objects.all()
    return render(request, 'accounts/role_list.html', locals())


@login_required
@permission_verify()
def role_edit(request, ids):
    iRole = RoleList.objects.get(id=ids)
    if request.method == "POST":
        form = RoleListForm(request.POST, instance=iRole)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('role_list'))
    else:
        form = RoleListForm(instance=iRole)

    kwvars = {
        'ids': ids,
        'form': form,
        'request': request,
    }

    return render(request, 'accounts/role_edit.html', kwvars)


@login_required
@permission_verify()
def role_del(request, ids):
    RoleList.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('role_list'))

