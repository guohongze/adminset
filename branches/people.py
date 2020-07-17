#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from branches.models import Region, People
from branches.forms import RegionForm, PeopleForm
from accounts.permission import permission_verify


@login_required()
@permission_verify()
def people_list(request):
    p = People.objects.all()
    results = {
        'people':  p,
    }
    return render(request, 'branches/people_list.html', results)


@login_required
@permission_verify()
def people_del(request):
    people_id = request.GET.get('id', '')
    if people_id:
        People.objects.filter(id=people_id).delete()

    people_id_all = str(request.POST.get('people_id_all', ''))
    if people_id_all:
        for people_id in people_id_all.split(','):
            People.objects.filter(id=people_id).delete()

    return HttpResponseRedirect(reverse('people_list'))


@login_required
@permission_verify()
def people_add(request):
    if request.method == 'POST':
        form = PeopleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('peple_list'))
    else:
        form = PeopleForm()

    results = {
        'form': form,
        'request': request,
    }
    return render(request, 'branches/people_base.html', results)


@login_required
@permission_verify()
def people_edit(request, people_id):
    people_obj = get_object_or_404(people, pk=people_id)
    if request.method == 'POST':
        form = PeopleForm(request.POST, instance=people_obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('people_list'))
    else:
        form = PeopleForm(instance=people_obj)

    results = {
        'form': form,
        'people_id': people_id,
        'request': request,
    }
    return render(request, 'branches/people_base.html', results)




