#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, RequestContext, redirect
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from cmdb.api import get_object
from forms import PeriodicTaskForm, IntervalForm


@login_required
@permission_verify()
def index(request):
    temp_name = "setup/setup-header.html"
    jobs_info = PeriodicTask.objects.all()
    return render_to_response('setup/job_list.html', locals(), RequestContext(request))


@login_required
@permission_verify()
def job_edit(request, ids):
    status = 0
    obj = get_object(PeriodicTask, id=ids)

    if request.method == 'POST':
        form = PeriodicTaskForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            status = 1
        else:
            status = 2
    else:
        form = PeriodicTaskForm(instance=obj)

    return render_to_response('setup/job_edit.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def job_add(request):
    temp_name = "setup/setup-header.html"
    if request.method == "POST":
        a_form = PeriodicTaskForm(request.POST)
        if a_form.is_valid():
            a_form.save()
            tips = u"增加成功！"
            display_control = ""
            return redirect("/setup/job/list/")
        else:
            tips = u"增加失败！"
            display_control = ""
            return render_to_response("setup/job_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        a_form = PeriodicTaskForm()
        return render_to_response("setup/job_add.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def job_del(request):
    temp_name = "setup/setup-header.html"
    if request.method == 'POST':
        jobs = request.POST.getlist('idc_check', [])
        if jobs:
            for n in jobs:
                PeriodicTask.objects.filter(id=n).delete()
    jobs_info = PeriodicTask.objects.all()
    return render_to_response("setup/job_list.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def job_interval_list(request):
    temp_name = "setup/setup-header.html"
    interval_info = IntervalSchedule.objects.all()
    return render_to_response('setup/interval_list.html', locals(), RequestContext(request))


@login_required
@permission_verify()
def job_interval_edit(request, ids):
    status = 0
    obj = get_object(IntervalSchedule, id=ids)

    if request.method == 'POST':
        form = IntervalForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            status = 1
        else:
            status = 2
    else:
        form = IntervalForm(instance=obj)

    return render_to_response('setup/interval_edit.html', locals(), RequestContext(request))


@login_required
@permission_verify()
def job_interval_del(request):
    temp_name = "setup/setup-header.html"
    if request.method == 'POST':
        intervals = request.POST.getlist('idc_check', [])
        if intervals:
            for n in intervals:
                IntervalSchedule.objects.filter(id=n).delete()
    interval_info = IntervalSchedule.objects.all()
    return render_to_response("setup/interval_list.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def job_interval_add(request):
    temp_name = "setup/setup-header.html"
    if request.method == "POST":
        a_form = IntervalForm(request.POST)
        if a_form.is_valid():
            a_form.save()
            tips = u"增加成功！"
            display_control = ""
            return redirect("/setup/job/interval/list/")
        else:
            tips = u"增加失败！"
            display_control = ""
            return render_to_response("setup/interval_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        a_form = IntervalForm()
        return render_to_response("setup/interval_add.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def job_crontab(request):
    pass