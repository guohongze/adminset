#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from appconf.models import Project
from forms import ProjectForm
from accounts.permission import permission_verify
import csv
import datetime
from cmdb.api import str2gb


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


@login_required
@permission_verify()
def project_export(request):
    export = request.GET.get("export", '')
    project_id_list = request.GET.getlist("id", '')
    if export == "part":
        if project_id_list:
            project_find = []
            for project_id in project_id_list:
                project_item = Project.objects.get(id=project_id)
                if project_item:
                    project_find.append(project_item)

    if export == "all":
        project_find = Project.objects.all()

    response = HttpResponse(content_type='text/csv')
    now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
    file_name = 'adminset_project_' + now + '.csv'
    response['Content-Disposition'] = "attachment; filename="+file_name
    writer = csv.writer(response)
    writer.writerow([str2gb(u'项目名称'), str2gb(u'项目描述'), str2gb(u'语言类型'), str2gb(u'程序类型'),
                     str2gb(u'服务器类型'), str2gb(u'程序框架'), str2gb(u'源类型'), str2gb(u'源地址'),
                     str2gb(u'程序部署路径'), str2gb(u'配置文件路径'),
                     str2gb(u'所属产品线'), str2gb(u'项目负责人'), str2gb(u'服务器')])
    for p in project_find:
        server_array = p.serverList
        server_result = ""
        for server in p.serverList.all():
            server_result += server.hostname+"\n"
        writer.writerow([str2gb(p.name), str2gb(p.description), p.language_type, p.app_type, p.server_type,
                        p.app_arch, p.source_type, p.source_address, p.appPath, p.configPath, str2gb(p.product),
                         str2gb(p.owner), str2gb(server_result)])
    return response
