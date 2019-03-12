#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views, ansible, shell, jobs


urlpatterns = [
    url(r'^ansible/$', ansible.index, name='ansible'),
    url(r'^shell/$', shell.index, name='shell'),
    url(r'^joblist/$', jobs.index, name='job_list'),
    url(r'^jobadd/$', jobs.job_add, name='job_add'),
    url(r'^jobdel/$', jobs.job_del, name='job_del'),
    url(r'^jobedit/(?P<ids>\d+)/$', jobs.job_edit, name='job_edit'),
    url(r'^jobintervallist/$', jobs.job_interval_list, name='job_interval_list'),
    url(r'^jobintervaladd/$', jobs.job_interval_add, name='job_interval_add'),
    url(r'^jobintervaldel/$', jobs.job_interval_del, name='job_interval_del'),
    url(r'^jobintervaledit/(?P<ids>\d+)/$', jobs.job_interval_edit, name='job_interval_edit'),
    url(r'^jobcrontablist/$', jobs.job_crontab_list, name='job_crontab_list'),
    url(r'^jobcrontabadd/$', jobs.job_crontab_add, name='job_crontab_add'),
    url(r'^jobcrontabdel/$', jobs.job_crontab_del, name='job_crontab_del'),
    url(r'^jobcrontabedit/(?P<ids>\d+)/$', jobs.job_crontab_edit, name='job_crontab_edit'),
    url(r'^jobresultlist/$', jobs.job_result_list, name='job_result_list'),
    url(r'^jobresultdel/$', jobs.job_result_del, name='job_result_del'),
    url(r'^jobbackend/$', jobs.job_backend, name='job_backend'),
    url(r'^jobbackend/task/(?P<name>\w+)/(?P<action>\w+)$', jobs.job_backend_task, name='job_backend_task'),
    url(r'^jobresultedit/(?P<ids>\d+)/$', jobs.job_result_edit, name='job_result_edit'),
    url(r'^scriptsexec/$', shell.exec_scripts, name='exec_scripts'),
    url(r'^playbook/$', ansible.playbook, name='playbook'),
    url(r'^hostsync/$', ansible.host_sync, name='host_sync'),
    url(r'^ansibleinfo/$', ansible.ansibleinfo, name='ansibleinfo'),
    url(r'^ansiblepage/$', ansible.logpage, name='ansiblepage'),
    url(r'^shellinfo/$', shell.shellinfo, name='shellinfo'),
    url(r'^shellpage/$', shell.logpage, name='shellpage'),
    url(r'^execstatus/(?P<exec_type>\d+)/$', ansible.exec_status, name='exec_status'),
]