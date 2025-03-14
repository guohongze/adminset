from django.urls import path, re_path
from . import views, ansible, shell, jobs


urlpatterns = [
    path('ansible/', ansible.index, name='ansible'),
    path('shell/', shell.index, name='shell'),
    path('joblist/', jobs.index, name='job_list'),
    path('jobadd/', jobs.job_add, name='job_add'),
    path('jobdel/', jobs.job_del, name='job_del'),
    re_path(r'^jobedit/(?P<ids>\d+)/$', jobs.job_edit, name='job_edit'),
    path('jobintervallist/', jobs.job_interval_list, name='job_interval_list'),
    path('jobintervaladd/', jobs.job_interval_add, name='job_interval_add'),
    path('jobintervaldel/', jobs.job_interval_del, name='job_interval_del'),
    re_path(r'^jobintervaledit/(?P<ids>\d+)/$', jobs.job_interval_edit, name='job_interval_edit'),
    path('jobcrontablist/', jobs.job_crontab_list, name='job_crontab_list'),
    path('jobcrontabadd/', jobs.job_crontab_add, name='job_crontab_add'),
    path('jobcrontabdel/', jobs.job_crontab_del, name='job_crontab_del'),
    re_path(r'^jobcrontabedit/(?P<ids>\d+)/$', jobs.job_crontab_edit, name='job_crontab_edit'),
    path('jobresultlist/', jobs.job_result_list, name='job_result_list'),
    path('jobresultdel/', jobs.job_result_del, name='job_result_del'),
    path('jobbackend/', jobs.job_backend, name='job_backend'),
    re_path(r'^jobbackend/task/(?P<n>\w+)/(?P<action>\w+)$', jobs.job_backend_task, name='job_backend_task'),
    re_path(r'^jobresultedit/(?P<ids>\d+)/$', jobs.job_result_edit, name='job_result_edit'),
    path('scriptsexec/', shell.exec_scripts, name='exec_scripts'),
    path('playbook/', ansible.playbook, name='playbook'),
    path('hostsync/', ansible.host_sync, name='host_sync'),
    path('ansibleinfo/', ansible.ansibleinfo, name='ansibleinfo'),
    path('ansiblepage/', ansible.logpage, name='ansiblepage'),
    path('shellinfo/', shell.shellinfo, name='shellinfo'),
    path('shellpage/', shell.logpage, name='shellpage'),
    re_path(r'^execstatus/(?P<exec_type>\d+)/$', ansible.exec_status, name='exec_status'),
]