#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, HttpResponse, redirect
import ConfigParser
import os
from django.contrib.auth.decorators import login_required


@login_required()
def index(request):
    temp_name = "config/config-header.html"
    # dirs = os.path.split(os.path.realpath(__file__))[0]
    dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = ConfigParser.ConfigParser()
    with open(dirs+'/adminset.conf', 'r') as cfgfile:
        config.readfp(cfgfile)
        a_path = config.get('config', 'ansible_path')
        r_path = config.get('config', 'roles_path')
        p_path = config.get('config', 'playbook_path')
        s_path = config.get('config', 'scripts_path')
    return render_to_response('config/index.html', locals())


@login_required()
def config_save(request):
    temp_name = "config/config-header.html"
    if request.method == 'POST':
        ansible_path = request.POST.get('ansible_path')
        roles_path = request.POST.get('roles_path')
        pbook_path = request.POST.get('pbook_path')
        scripts_path = request.POST.get('scripts_path')
        config = ConfigParser.RawConfigParser()
        dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config.add_section('config')
        config.set('config', 'ansible_path', ansible_path)
        config.set('config', 'roles_path', roles_path)
        config.set('config', 'playbook_path', pbook_path)
        config.set('config', 'scripts_path', scripts_path)
        with open(dirs+'/adminset.conf', 'wb') as cfgfile:
            config.write(cfgfile)
        with open(dirs+'/adminset.conf', 'r') as cfgfile:
            config.readfp(cfgfile)
            a_path = config.get('config', 'ansible_path')
            r_path = config.get('config', 'roles_path')
            p_path = config.get('config', 'playbook_path')
            s_path = config.get('config', 'scripts_path')
        return render_to_response('config/index.html', locals())


def get_dir(args):
    config = ConfigParser.RawConfigParser()
    dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(dirs+'/adminset.conf', 'r') as cfgfile:
        config.readfp(cfgfile)
        a_path = config.get('config', 'ansible_path')
        r_path = config.get('config', 'roles_path')
        p_path = config.get('config', 'playbook_path')
        s_path = config.get('config', 'scripts_path')
    if args == "a_path":
        return a_path
    if args == "r_path":
        return r_path
    if args == "p_path":
        return p_path
    if args == "s_path":
        return s_path
