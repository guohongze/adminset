from subprocess import Popen, PIPE
from cmdb.models import Host, HostGroup
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse


def ansible(request):
    temp_name = "ansible/ansible-header.html"
    all_host = Host.objects.all()
    all_group = HostGroup.objects.all()
    return render_to_response('ansible/index.html', locals())


def ansible_exec(request):
    if request.method == 'POST':
        host = request.POST.getlist('mserver', [])
        group = request.POST.getlist('mgroup', [])
        playbook = request.POST.getlist('mplaybook', [])
        command = request.POST.getlist('mcommand', [])
    if host:
        if playbook:
            for h in host:
                print h
                f = open('svn_install.yml', 'r+')
                flist = f.readlines()
                flist[0] = '- hosts: '+h+'\n'
                f = open('svn_install.yml', 'w+')
                f.writelines(flist)
                f.close()
                cmd = "ansible-playbook"+" "+playbook
                p = Popen(cmd, stdout=PIPE, shell=True)
                data = p.communicate()[0]
                print data
        else:
            for h in host:
                cmd = "ansible"+" "+h+" "+"-a"+" "+command
                print cmd
                p = Popen(cmd, stdout=PIPE, shell=True)
                data = p.communicate()[0]
                print data
    if group:
        if playbook:
            for g in group:
                print g
                f = open('svn_install.yml', 'r+')
                flist = f.readlines()
                flist[0] = '- hosts: '+g+'\n'
                f = open('svn_install.yml', 'w+')
                f.writelines(flist)
                f.close()
                cmd = "ansible-playbook"+" "+playbook
                p = Popen(cmd, stdout=PIPE, shell=True)
                data = p.communicate()[0]
                print data
        else:
            for g in group:
                cmd = "ansible"+" "+g+" "+"-a"+" "+command
                print cmd
                p = Popen(cmd, stdout=PIPE, shell=True)
                data = p.communicate()[0]
                print data
    return HttpResponse("ok")

