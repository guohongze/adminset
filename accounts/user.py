#! /usr/bin/env python
# -*- coding: utf-8 -*-
# update by guohongze@126.com
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .forms import LoginUserForm, EditUserForm, ChangePasswordForm
from django.contrib.auth import get_user_model
from .forms import AddUserForm
from django.core.urlresolvers import reverse
from accounts.permission import permission_verify


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'GET' and request.GET.has_key('next'):
        next_page = request.GET['next']
    else:
        next_page = '/'
    if next_page == "/accounts/logout/":
        next_page = '/'
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(request.POST['next'])
    else:
        form = LoginUserForm(request)
    kwargs = {
        'request': request,
        'form':  form,
        'next': next_page,
    }
    return render(request, 'accounts/login.html', kwargs)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
@permission_verify()
def user_list(request):
    temp_name = "accounts/accounts-header.html"
    all_user = get_user_model().objects.all()
    kwargs = {
        'temp_name': temp_name,
        'all_user':  all_user,
    }
    return render(request, 'accounts/user_list.html', kwargs)


@login_required
@permission_verify()
def user_add(request):
    temp_name = "accounts/accounts-header.html"
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()
            return HttpResponseRedirect(reverse('user_list'))
    else:
        form = AddUserForm()
    kwargs = {
        'form': form,
        'request': request,
        'temp_name': temp_name,
    }
    return render(request, 'accounts/user_add.html', kwargs)


@login_required
@permission_verify()
def user_del(request, ids):
    if ids:
        get_user_model().objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('user_list'))


@login_required
@permission_verify()
def user_edit(request, ids):
    user = get_user_model().objects.get(id=ids)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            status = 1
        else:
            status = 2
    else:
        form = EditUserForm(instance=user)
    return render(request, 'accounts/user_edit.html', locals())


@login_required
@permission_verify()
def reset_password(request, ids):
    user = get_user_model().objects.get(id=ids)
    newpassword = get_user_model().objects.make_random_password(length=10, allowed_chars='abcdefghjklmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY3456789')
    print('====>ResetPassword:{}-->{}'.format(user.username, newpassword))
    user.set_password(newpassword)
    user.save()
    kwargs = {
        'object': user,
        'newpassword': newpassword,
        'request': request,
    }
    return render(request, 'accounts/reset_password.html', kwargs)


@login_required
def change_password(request):
    temp_name = "accounts/accounts-header.html"
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('logout'))
    else:
        form = ChangePasswordForm(user=request.user)
    kwargs = {
        'form': form,
        'request': request,
        'temp_name': temp_name,
    }
    return render(request, 'accounts/change_password.html', kwargs)
