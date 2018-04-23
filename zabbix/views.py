#!/usr/bin/env python
# -*- coding:utf-8 -*-

from jsonrpc import jsonrpc_method
from jsonrpc.proxy import ServiceProxy
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from zabbix_api import *
from lib.db import *
from lib.util import *

level = get_dir("log_level")
log_path = get_dir("log_path")
log("zabbix.log", level, "/Users/lvhaidong/Desktop/main/logs/")


def listapi(request):
    method = request.GET.get('method')
    if method == "zbhost_allhost":
        s = ServiceProxy('http://127.0.0.1:8000/zabbix/json/')
        data = s.zbhost_allhost.getlist()
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
    elif method == "zabbix_gettem":
        s = ServiceProxy('http://127.0.0.1:8000/zabbix/json/')
        tem = s.zabbix_gettem.getlist()
        return HttpResponse(json.dumps(tem), content_type='application/json; charset=utf-8')
    elif method == "zabbix_tem":
        s = ServiceProxy('http://127.0.0.1:8000/zabbix/json/')
        host_tem = s.zabbix_tem.getlist()
        return HttpResponse(json.dumps(host_tem), content_type='application/json; charset=utf-8')
    elif method == "zbhost":
        s = ServiceProxy('http://127.0.0.1:8000/zabbix/json/')
        zbhost = s.zbhost.getlist()
        return HttpResponse(json.dumps(zbhost), content_type='application/json; charset=utf-8')
    elif method == "zabbix":
        s = ServiceProxy('http://127.0.0.1:8000/zabbix/json/')
        zabbixhost = s.zabbix.getlist()
        return HttpResponse(json.dumps(zabbixhost), content_type='application/json; charset=utf-8')
    else:
        data = {
            u'result': u'{"code": 1, "result": [{"host": "meidai-monitor", "hostid": "10291"}]}',
            u'jsonrpc': u'1.0', u'id': u'48e8787a-ad68-11e7-be94-000c29a6a1c8', u'error': None}
        data1 = json.dumps(data)
        return HttpResponse(json.dumps(data))


def getapi(request):
    method = request.GET.get('method')
    data = {}
    data['method'] = method + '.get'
    data['params'] = {
        "m_table": request.GET.get('m_table', None),
        'field': request.GET.get('field', None),
        's_table': request.GET.get('s_table', None),
        'where': {'host': request.GET.get('ip')}
    }
    if method == "graph":
        s = ServiceProxy('http://127.0.0.1:8000/zabbix/json/')
        zbx_graph = s.graph.get(data)
        return HttpResponse(json.dumps(zbx_graph))


@csrf_exempt
def zabbixapi(request):
    method = request.POST.get('method')
    hostids = request.POST.get('hostids')
    groupid = request.POST.get('groupid')
    data = {}
    data['method'] = 'zabbix.' + method
    data['params'] = {
        "hostids": hostids,
        "groupid": groupid
    }
    if data['method'] == "zabbix.link_tem":
        s = ServiceProxy('http://127.0.0.1:8000/zabbix/json/')
        link_tem = s.zabbix.link_tem(data)
        return HttpResponse(json.dumps(link_tem))
    elif data['method'] == "zabbix.add":
        s = ServiceProxy('http://127.0.0.1:8000/zabbix/json/')
        create_zbx_host = s.zabbix.add(data)
        return HttpResponse(json.dumps(create_zbx_host))


@csrf_exempt
def zabbix_template(request):
    method = request.POST.get('method')
    hostid = request.POST.get('hostid')
    templateid = request.POST.get('templateid')
    data = {}
    data['method'] = 'zabbix_template.' + method
    data['params'] = {
        "hostids": hostid,
        "templateid": templateid
    }
    if data['method'] == "zabbix_template.unlink_tem":
        s = ServiceProxy('http://127.0.0.1:8000/zabbix/json/')
        unlink_tem = s.zabbix_template.unlink_tem(data)
        return HttpResponse(json.dumps(unlink_tem))


@jsonrpc_method('graph.get')
def graph_get(request, arg1):
    ret = []
    stime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data_where = {}
    # add centos7 "Network traffic on ens33"
    monitor_name = ["CPU load", "CPU utilization", "Memory usage", "Disk space usage /", "Network traffic on eth0",
                    "Network traffic on em1", "Network traffic on ens33", "MongoDB Memory", 'MongoDB Networks']
    output = ['hostid']
    data = arg1['params']
    fields = data.get('output', output)
    where = data.get('where', None)
    data_where['host'] = where['host']
    if not where:
        return json.dumps({'code': 1, 'errmsg': 'must need a condition'})
    graph_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../static/zabbix'))
    config = os.path.dirname(os.path.dirname(__file__)) + "/adminset.conf"
    mysql_config = get_config(config, section='zbmysql')
    result = Cursor(mysql_config).get_one_result('hosts', fields, data_where)  # SELECT hostid FROM hosts WHERE host=ip
    login_url = get_dir('login_url')
    graph_url = get_dir('graph')
    flag, zabbix = auth()
    if flag:
        graphs = zabbix.get_graphid(str(result['hostid']))
        print(graphs)
        for graph in graphs:
            if graph['name'] in monitor_name:
                ph = GraphDownload(login_url, graph_url)
                ret_data = ph.get_graph(graph['graphid'], stime,
                                        image_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                               '../static/zabbix'))
                ret.append(ret_data)
        img_url = graph_img(os.path.dirname(os.path.dirname(__file__)) +'/static/zabbix')
        return json.dumps({'code': 0, 'result': img_url})
    else:
        return json.dumps({'code': -1, 'errmsg': 'create zabbix faild!'})


@jsonrpc_method('zabbix.add')
def zabbix_add(request, arg1):
    data = arg1['params']
    hosts = data['hostids'].split(",")
    url = get_dir("zabbix_url")
    user = get_dir("zabbix_user")
    password = get_dir("zabbix_passwd")
    zabbix = ZabbixAction(url, user, password)
    result = zabbix.create_zabbix_host(hosts, data['groupid'], url, user, password)
    if len(result):
        return json.dumps({'code': 0, 'result': 'create zabbix host %s scucess' % result[0]['hostids']})
    else:
        return json.dumps({'code': -1, 'result': 'create zabbix faild!'})


@jsonrpc_method('zabbix.getlist')
def zabbix_select(request):
    flag, zabbix = auth()
    if flag:
        hostgroup = zabbix.get_hostgroup()
        return json.dumps({'code': 0, 'result': hostgroup})
    else:
        return json.dumps({'code': 0, 'result': "Not Login!"})


@jsonrpc_method('zbhost.getlist')
def zbhost_select(request):
    value = insert_ip()
    print(value)
    config = os.path.dirname(os.path.dirname(__file__)) + "/adminset.conf"
    mysql_config = get_config(config)
    del mysql_config['engine']
    mysql_config['passwd'] = mysql_config.pop('password')
    mysql_config['db'] = mysql_config.pop('database')
    # result = Cursor(mysql_config).get_results('cmdb_host', ['ip', 'id'])
    result = Cursor(mysql_config).get_results('zabbix_host', ['ip', 'id'])
    return json.dumps({"code": 0, "result": result})


@jsonrpc_method('zabbix_template.unlink_tem')
def zabbix_unlink_tem(request, arg1):
    result = []
    data = arg1['params']
    data_host = data['hostids'].split(',')
    flag, zabbix = auth()
    if flag:
        for i in data_host:
            result.append(zabbix.unlink_template(int(i), data['templateid']))
        return json.dumps({'code': 0, 'result': result})
    else:
        return json.dumps({'code': -1, 'result': "Not Login!"})


@jsonrpc_method('zabbix.link_tem')
def zabbix_link_tem(request, arg1):
    result = []
    template = {}
    data = arg1['params']
    if len(data['hostids']):
        data_host = data['hostids'].split(',')
        flag, zabbix = auth()
        if flag:
            for i in data_host:
                if len(zabbix.hostid_get_template(i)[0]['parentTemplates']) == 0:
                    result.append(zabbix.link_template(int(i), data['groupid']))
                else:
                    template['templateid'] = data['groupid']
                    data_mu = zabbix.hostid_get_template(i)[0]['parentTemplates']
                    data_mu.append(template)
                    result.append(zabbix.link_template(int(i), data_mu))
                return json.dumps({'code': 0, 'result': result})
        else:
            return json.dumps({'code': -1, 'errmsg': "Not Login!"})
    else:
        return json.dumps({'code': 1, 'errmsg': "Not select hostid!"})


@jsonrpc_method('zbhost_allhost.getlist')
def zbhost_allhost_select(request):
    url = get_dir("zabbix_url")
    user = get_dir("zabbix_user")
    password = get_dir("zabbix_passwd")
    zabbix = ZabbixAction(url, user, password)
    flag = zabbix.login()
    if flag:
        data = zabbix.get_hosts()
        return json.dumps({'code': 0, 'result': data})
    else:
        return json.dumps({'code': -1, 'result': "Not Login!"})


@jsonrpc_method('zabbix_gettem.getlist')
def zabbix_gettem_select(request):
    url = get_dir("zabbix_url")
    user = get_dir("zabbix_user")
    password = get_dir("zabbix_passwd")
    zabbix = ZabbixAction(url, user, password)
    flag = zabbix.login()
    if flag:
        data = zabbix.get_template()
        return json.dumps({'code': 0, 'result': data})
    else:
        return json.dumps({'code': -1, 'result': "Not Login!"})


@jsonrpc_method('zabbix_tem.getlist')
def zabbix_gettem_select(request):
    url = get_dir("zabbix_url")
    user = get_dir("zabbix_user")
    password = get_dir("zabbix_passwd")
    zabbix = ZabbixAction(url, user, password)
    flag = zabbix.login()
    if flag:
        data = zabbix.get_host_tem()
        return json.dumps({'code': 0, 'result': data})
    else:
        return json.dumps({'code': -1, 'result': "Not Login!"})


def auth():
    url = get_dir("zabbix_url")
    user = get_dir("zabbix_user")
    password = get_dir("zabbix_passwd")
    zabbix = ZabbixAction(url, user, password)
    flag = zabbix.login()
    return flag, zabbix


def select_cmdb_host():
    config = os.path.dirname(os.path.dirname(__file__)) + "/adminset.conf"
    mysql_config = get_config(config)
    del mysql_config['engine']
    mysql_config['user'] = mysql_config.pop('user')
    mysql_config['passwd'] = mysql_config.pop('password')
    mysql_config['db'] = mysql_config.pop('database')
    ips = Cursor(mysql_config).get_results('cmdb_host', ['ip'])
    result = []
    for ip in ips:
        result.append(ip['ip'])
    return result


def select_hosts():
    config = os.path.dirname(os.path.dirname(__file__)) + "/adminset.conf"
    mysql_config = get_config(config, "zbmysql")
    hosts = Cursor(mysql_config).get_results('hosts', ['host'])
    result = []
    for host in hosts:
        result.append(host['host'])
    return result


def test(request):
    value = insert_ip()
    return HttpResponse(json.dumps({"result": value}))


def insert_ip():
    config = os.path.dirname(os.path.dirname(__file__)) + "/adminset.conf"
    mysql_config = get_config(config)
    del mysql_config['engine']
    mysql_config['user'] = mysql_config.pop('user')
    mysql_config['passwd'] = mysql_config.pop('password')
    mysql_config['db'] = mysql_config.pop('database')
    # clear zabbix_host table
    Cursor(mysql_config).execute_clean_sql('zabbix_host')

    ips = list(set(select_cmdb_host()).difference(set(select_hosts())))
    if len(ips) == 0:
        return "没有新增的数据"

    for ip in ips:
        result = Cursor(mysql_config).execute_insert_sql1('zabbix_host', ip)

    return "插入完成"

