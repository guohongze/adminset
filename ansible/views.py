from subprocess import Popen, PIPE
from cmdb.models import Host, HostGroup
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse


def ansible(request):
    host_list = Host.objects.all()
    hostgroup = HostGroup.objects.all()
    return render_to_response('ansible.html',locals())


def ansiblexe(request):
    if request.method == 'POST':
        host1 = request.POST.getlist('mserver', [])
        group = request.POST.getlist('mgroup', [])
        playbook = request.POST.getlist('mplaybook', [])
        command = request.POST.getlist('mcommand', [])
        for h in host1:
            print h
        print type(group)
        print type(playbook)
        print type(command)
    return HttpResponse("ok")
        # if host:
        #     if playbook:
        #         for h in host:
        #             print h
        #             f = open('svn_install.yml', 'r+')
        #             flist = f.readlines()
        #             flist[0] = '- hosts: '+h+'\n'
        #             f = open('svn_install.yml', 'w+')
        #             f.writelines(flist)
        #             f.close()
        #             cmd = "ansible-playbook"+" "+playbook
        #             p = Popen(cmd, stdout=PIPE, shell=True)
        #             data = p.communicate()
        #         return data
        #     else:
        #         for h in host:
        #             cmd = "ansible" + " " + h + "-a" + command
        #             p = Popen(cmd, stdout=PIPE, shell=True)
        #             data = p.communicate()
        #         return data
        # else:
        #     if group:
        #         for g in group:
        #             f = open('svn_install.yml', 'r+')
        #             flist = f.readlines()
        #             flist[0] = '- hosts: '+g+'\n'
        #             f = open('svn_install.yml', 'w+')
        #             f.writelines(flist)
        #             f.close
        #             cmd = "ansible-playbook"+" "+playbook
        #             p = Popen(cmd, stdout=PIPE, shell=True)
        #             data = p.communicate()
        #         return data
        #      else:
        #         for g in group:
        #             cmd = "ansible" + " " + h + "-a" + command
        #             p = Popen(cmd, stdout=PIPE, shell=True)
        #             data = p.communicate()
        #         return data

