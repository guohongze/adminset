#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, HttpResponse, redirect, RequestContext
import ConfigParser
import os
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from django.contrib.auth import get_user_model
import logging
from lib.log import dic


@login_required()
@permission_verify()
def index(request):
    temp_name = "config/config-header.html"
    display_control = "none"
    # dirs = os.path.split(os.path.realpath(__file__))[0]
    dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = ConfigParser.ConfigParser()
    all_level = dic
    with open(dirs+'/adminset.conf', 'r') as cfgfile:
        config.readfp(cfgfile)
        a_path = config.get('config', 'ansible_path')
        r_path = config.get('config', 'roles_path')
        p_path = config.get('config', 'playbook_path')
        s_path = config.get('config', 'scripts_path')
        engine = config.get('db', 'engine')
        host = config.get('db', 'host')
        port = config.get('db', 'port')
        user = config.get('db', 'user')
        password = config.get('db', 'password')
        database = config.get('db', 'database')
        token = config.get('token', 'token')
        log_path = config.get('log', 'log_path')
        log_level = config.get('log', 'log_level')
    return render_to_response('config/index.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def config_save(request):
    temp_name = "config/config-header.html"
    if request.method == 'POST':
        # path
        ansible_path = request.POST.get('ansible_path')
        roles_path = request.POST.get('roles_path')
        pbook_path = request.POST.get('pbook_path')
        scripts_path = request.POST.get('scripts_path')
        # db
        engine = request.POST.get('engine')
        host = request.POST.get('host')
        port = request.POST.get('port')
        user = request.POST.get('user')
        password = request.POST.get('password')
        database = request.POST.get('database')
        # cmdb_api_token
        token = request.POST.get('token')
        # log
        log_path = request.POST.get('log_path')
        log_level = request.POST.get('log_level')
        
        config = ConfigParser.RawConfigParser()
        dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config.add_section('config')
        config.set('config', 'ansible_path', ansible_path)
        config.set('config', 'roles_path', roles_path)
        config.set('config', 'playbook_path', pbook_path)
        config.set('config', 'scripts_path', scripts_path)
        config.add_section('db')
        config.set('db', 'engine', engine)
        config.set('db', 'host', host)
        config.set('db', 'port', port)
        config.set('db', 'user', user)
        config.set('db', 'password', password)
        config.set('db', 'database', database)
        config.add_section('token')
        config.set('token', 'token', token)
        config.add_section('log')
        config.set('log', 'log_path', log_path)
        config.set('log', 'log_level', log_level)
        tips = u"保存成功！"
        display_control = ""
        with open(dirs+'/adminset.conf', 'wb') as cfgfile:
            config.write(cfgfile)
        with open(dirs+'/adminset.conf', 'r') as cfgfile:
            config.readfp(cfgfile)
            a_path = config.get('config', 'ansible_path')
            r_path = config.get('config', 'roles_path')
            p_path = config.get('config', 'playbook_path')
            s_path = config.get('config', 'scripts_path')
            engine = config.get('db', 'engine')
            host = config.get('db', 'host')
            port = config.get('db', 'port')
            user = config.get('db', 'user')
            password = config.get('db', 'password')
            database = config.get('db', 'database')
            token = config.get('token', 'token')
            log_path = config.get('log', 'log_path')
    else:
        display_control = "none"
    return render_to_response('config/index.html', locals(), RequestContext(request))


def get_dir(args):
    config = ConfigParser.RawConfigParser()
    dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(dirs+'/adminset.conf', 'r') as cfgfile:
        config.readfp(cfgfile)
        a_path = config.get('config', 'ansible_path')
        r_path = config.get('config', 'roles_path')
        p_path = config.get('config', 'playbook_path')
        s_path = config.get('config', 'scripts_path')
        token = config.get('token', 'token')
        log_path = config.get('log', 'log_path')
        log_level = config.get('log', 'log_level')

    if args == "a_path":
        return a_path
    if args == "r_path":
        return r_path
    if args == "p_path":
        return p_path
    if args == "s_path":
        return s_path
    if args == "token":
        return token
    if args == "log_path":
        return log_path
    if args == "log_level":
        return log_level


def get_token(request):
    if request.method == 'POST':
        new_token = get_user_model().objects.make_random_password(length=12, allowed_chars='abcdefghjklmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY3456789')
        return HttpResponse(new_token)
    else:
        return True
