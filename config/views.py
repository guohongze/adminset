#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
import ConfigParser
import os
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from django.contrib.auth import get_user_model
from lib.log import dic


@login_required()
@permission_verify()
def index(request):
    temp_name = "config/config-header.html"
    display_control = "none"
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
        ssh_pwd = config.get('token', 'ssh_pwd')
        log_path = config.get('log', 'log_path')
        log_level = config.get('log', 'log_level')
        mongodb_ip = config.get('mongodb', 'mongodb_ip')
        mongodb_port = config.get('mongodb', 'mongodb_port')
        mongodb_user = config.get('mongodb', 'mongodb_user')
        mongodb_pwd = config.get('mongodb', 'mongodb_pwd')
        mongodb_collection = config.get('mongodb', 'collection')
        webssh_domain = config.get('webssh', 'domain')
    return render(request, 'config/index.html', locals())


@login_required()
@permission_verify()
def config_save(request):
    temp_name = "config/config-header.html"
    if request.method == 'POST':
        # path info
        ansible_path = request.POST.get('ansible_path')
        roles_path = request.POST.get('roles_path')
        pbook_path = request.POST.get('pbook_path')
        scripts_path = request.POST.get('scripts_path')
        # db info
        engine = request.POST.get('engine')
        host = request.POST.get('host')
        port = request.POST.get('port')
        user = request.POST.get('user')
        password = request.POST.get('password')
        database = request.POST.get('database')
        # cmdb_api_token
        token = request.POST.get('token')
        ssh_pwd = request.POST.get('ssh_pwd')
        # log info
        log_path = request.POST.get('log_path')
        log_level = request.POST.get('log_level')
        # mongodb info
        mongodb_ip = request.POST.get('mongodb_ip')
        mongodb_port = request.POST.get('mongodb_port')
        mongodb_user = request.POST.get('mongodb_user')
        mongodb_pwd = request.POST.get('mongodb_pwd')
        mongodb_collection = request.POST.get('mongodb_collection')
        # webssh domain
        webssh_domain = request.POST.get('webssh_domain')

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
        config.set('token', 'ssh_pwd', token)
        config.add_section('log')
        config.set('log', 'log_path', log_path)
        config.set('log', 'log_level', log_level)
        config.add_section('mongodb')
        config.set('mongodb', 'mongodb_ip', mongodb_ip)
        config.set('mongodb', 'mongodb_port', mongodb_port)
        config.set('mongodb', 'mongodb_user', mongodb_user)
        config.set('mongodb', 'mongodb_pwd', mongodb_pwd)
        config.set('mongodb', 'collection', mongodb_collection)
        config.add_section('webssh')
        config.set('webssh', 'domain', webssh_domain)
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
            ssh_pwd = config.get('token', 'ssh_pwd')
            log_path = config.get('log', 'log_path')
            mongodb_ip = config.get('mongodb', 'mongodb_ip')
            mongodb_port = config.get('mongodb', 'mongodb_port')
            mongodb_user = config.get('mongodb', 'mongodb_user')
            mongodb_pwd = config.get('mongodb', 'mongodb_pwd')
            mongodb_collection = config.get('mongodb', 'collection')
            webssh_domain = config.get('webssh', 'domain')
    else:
        display_control = "none"
    return render(request, 'config/index.html', locals())


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
        ssh_pwd = config.get('token', 'ssh_pwd')
        log_path = config.get('log', 'log_path')
        log_level = config.get('log', 'log_level')
        mongodb_ip = config.get('mongodb', 'mongodb_ip')
        mongodb_port = config.get('mongodb', 'mongodb_port')
        mongodb_user = config.get('mongodb', 'mongodb_user')
        mongodb_pwd = config.get('mongodb', 'mongodb_pwd')
        mongodb_collection = config.get('mongodb', 'collection')
        webssh_domain = config.get('webssh', 'domain')
    # 根据传入参数返回变量以获取配置，返回变量名与参数名相同
    if args:
        return vars()[args]
    else:
        return HttpResponse(status=403)


@login_required()
@permission_verify()
def get_token(request):
    if request.method == 'POST':
        new_token = get_user_model().objects.make_random_password(length=12, allowed_chars='abcdefghjklmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY3456789')
        return HttpResponse(new_token)
    else:
        return True
