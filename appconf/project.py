#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from models import Project
from forms import ProjectForm
from accounts.permission import permission_verify


@login_required()
@permission_verify()
def project_list(request):
    temp_name = "appconf/appconf-header.html"
    all_project = Project.objects.all()
    results = {
        'temp_name': temp_name,
        'all_project':  all_project,
    }
    return render(request, 'appconf/project_list.html', results)


@login_required
@permission_verify()
def project_del(request):
    project_id = request.GET.get('project_id', '')
    if project_id:
        Project.objects.filter(id=project_id).delete()

    project_id_all = str(request.POST.get('project_id_all', ''))
    if project_id_all:
        for project_id in project_id_all.split(','):
            Project.objects.filter(id=project_id).delete()

    return HttpResponseRedirect(reverse('project_list'))


@login_required
@permission_verify()
def project_add(request):
    temp_name = "appconf/appconf-header.html"
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project_list'))
    else:
        form = ProjectForm()

    results = {
        'form': form,
        'request': request,
        'temp_name': temp_name,
    }
    return render(request, 'appconf/project_base.html', results)


@login_required
@permission_verify()
def project_edit(request, project_id):
    project = Project.objects.get(id=project_id)
    temp_name = "appconf/appconf-header.html"
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project_list'))
    else:
        form = ProjectForm(instance=project)

    results = {
        'form': form,
        'project_id': project_id,
        'request': request,
        'temp_name': temp_name,
    }
    return render(request, 'appconf/project_base.html', results)


