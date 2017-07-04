#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from django_celery_results.models import TaskResult
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from cmdb.api import get_object
from forms import PeriodicTaskForm, IntervalForm, CrontabForm, TaskResultForm
from subprocess import Popen, PIPE
import os, time


@login_required
@permission_verify()
def index(request):
    temp_name = "setup/setup-header.html"
    jobs_info = PeriodicTask.objects.all()
    return render(request, 'setup/job_list.html', locals())


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

    return render(request, 'setup/job_edit.html', locals())


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
            return render(request, "setup/job_add.html", locals())
    else:
        display_control = "none"
        a_form = PeriodicTaskForm()
        return render(request, "setup/job_add.html", locals())


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
    return render(request, "setup/job_list.html", locals())


@login_required()
@permission_verify()
def job_interval_list(request):
    temp_name = "setup/setup-header.html"
    interval_info = IntervalSchedule.objects.all()
    return render(request, 'setup/interval_list.html', locals())


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

    return render(request, 'setup/interval_edit.html', locals())


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
    return render(request, "setup/interval_list.html", locals())


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
            return render(request, "setup/interval_add.html", locals())
    else:
        display_control = "none"
        a_form = IntervalForm()
        return render(request, "setup/interval_add.html", locals())


@login_required()
@permission_verify()
def job_crontab_list(request):
    temp_name = "setup/setup-header.html"
    crontab_info = CrontabSchedule.objects.all()
    return render(request, 'setup/crontab_list.html', locals())


@login_required
@permission_verify()
def job_crontab_edit(request, ids):
    status = 0
    obj = get_object(CrontabSchedule, id=ids)

    if request.method == 'POST':
        form = CrontabForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            status = 1
        else:
            status = 2
    else:
        form = CrontabForm(instance=obj)

    return render(request, 'setup/crontab_edit.html', locals())


@login_required
@permission_verify()
def job_crontab_del(request):
    temp_name = "setup/setup-header.html"
    if request.method == 'POST':
        crontabs = request.POST.getlist('idc_check', [])
        if crontabs:
            for n in crontabs:
                CrontabSchedule.objects.filter(id=n).delete()
    crontab_info = CrontabSchedule.objects.all()
    return render(request, "setup/crontab_list.html", locals())


@login_required()
@permission_verify()
def job_crontab_add(request):
    temp_name = "setup/setup-header.html"
    if request.method == "POST":
        a_form = CrontabForm(request.POST)
        if a_form.is_valid():
            a_form.save()
            tips = u"增加成功！"
            display_control = ""
            return redirect("/setup/job/crontab/list/")
        else:
            tips = u"增加失败！"
            display_control = ""
            return render(request, "setup/crontab_add.html", locals())
    else:
        display_control = "none"
        a_form = CrontabForm()
        return render(request, "setup/crontab_add.html", locals())


@login_required()
@permission_verify()
def job_result_list(request):
    temp_name = "setup/setup-header.html"
    result_info = TaskResult.objects.all().order_by("-id")
    return render(request, 'setup/result_list.html', locals())


@login_required
@permission_verify()
def job_result_edit(request, ids):
    status = 0
    obj = get_object(TaskResult, id=ids)

    if request.method == 'POST':
        form = TaskResultForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            status = 1
        else:
            status = 2
    else:
        form = TaskResultForm(instance=obj)

    return render(request, 'setup/result_edit.html', locals())


@login_required
@permission_verify()
def job_result_del(request):
    temp_name = "setup/setup-header.html"
    if request.method == 'POST':
        results = request.POST.getlist('idc_check', [])
        if results:
            for n in results:
                TaskResult.objects.filter(id=n).delete()
    result_info = TaskResult.objects.all()
    return render(request, "setup/result_list.html", locals())


@login_required
@permission_verify()
def job_backend(request):
    temp_name = "setup/setup-header.html"
    celery_file = os.path.exists('/var/opt/adminset/pid/w1.pid')
    beat_file = os.path.exists('/var/opt/adminset/pid/beat.pid')
    if celery_file:
        celery_disable = "disabled"
        celery_stop_disable = ""
    else:
        celery_disable = ""
        celery_stop_disable = "disabled"
    if beat_file:
        beat_disable = "disabled"
        beat_stop_disable = ""
    else:
        beat_disable = ""
        beat_stop_disable = "disabled"
    return render(request, "setup/job_backend.html", locals())


@login_required
@permission_verify()
def job_backend_task(request, name, action):
    cmd = "service "+name+" "+action
    Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    time.sleep(3)
    return redirect("/setup/job/backend/")
