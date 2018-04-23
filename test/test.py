# coding:utf-8
import json

#
# from lib.db import Cursor
# from lib.util import get_config
# # from lib.db import *
# import os


def dict_diff():
    # list1 = select_cmdb_host()
    # list2 = select_hosts()

    list1 = [{'ip': '127.0.0.1'}, {'ip': '192.168.1.1'}, {'ip': '192.168.1.2'}]
    list2 = [{'ip': '127.0.0.1'}, {'ip': '192.168.1.3'}, {'ip': '192.168.1.4'}, {'ip': '192.168.1.5'}]

    re = dict()

    for d in list2:  # add values to each set() from dicts in list1
        if isinstance(d, dict):
            for k in d.keys():
                if k not in re.keys():
                    re[k] = set()
                re[k].add(d[k])

    for d in list1:  # remove values that in list_now's dicts
        if isinstance(d, dict):
            for k in d.keys():
                if d[k] in re[k]:
                    # print d[k]
                    re[k].remove(d[k])
                    # if len(re[k])>1:
                    #    re[k].remove(d[k])

    for item in re.keys():
        if re[item] == set([]):  # delete keys whose value is set(u'')
            print item
            del re[item]

    return re


# def insert_ip():
#     config = os.path.dirname(os.path.dirname(__file__)) + "/adminset.conf"
#     mysql_config = get_config(config)
#     del mysql_config['engine']
#     mysql_config['user'] = mysql_config.pop('user')
#     mysql_config['passwd'] = mysql_config.pop('password')
#     mysql_config['db'] = mysql_config.pop('database')
#     # clear zabbix_host table
#     Cursor(mysql_config).execute_clean_sql('zabbix_host')
#
#     ips = list(dict_diff()['ip'])
#     content_ip = {}
#     for ip in ips:
#         content_ip['ip'] = ip
#         result = Cursor(mysql_config).execute_insert_sql('zabbix_host', content_ip)
#
#     return "插入完成"
#
#
# def select_cmdb_host():
#     config = os.path.dirname(os.path.dirname(__file__)) + "/adminset.conf"
#     mysql_config = get_config(config)
#     del mysql_config['engine']
#     mysql_config['user'] = mysql_config.pop('user')
#     mysql_config['passwd'] = mysql_config.pop('password')
#     mysql_config['db'] = mysql_config.pop('database')
#     print(mysql_config)
#     result = Cursor(mysql_config).get_results('cmdb_host', ['ip'])
#     return result
#
#
# def select_hosts():
#     config = os.path.join(os.path.dirname(os.path.dirname(__file__)), "./adminset.conf")
#     mysql_config = get_config(config, "zbmysql")
#     result = Cursor(mysql_config).get_results('hosts', ['ip'])
#     return result


def list_replace_dict():
    list1 = [{"host": "127.0.0.1"}, {"host": "192.0.0.1"}]
    dict = {}
    list2 = []
    for i in range(len(list1)):
        dict['ip'] = list1[i]['host']
        list2.append(dict)
    print(list2)


def list_diff():
    list1 = [u'10.10.10.26', u'10.10.10.234']
    list2 = [u'10.10.10.201', u'10.10.10.233', u'10.10.10.234', u'10.10.10.26', u'114.215.195.35', u'Template MongoDB']
    print list(set(list1).difference(set(list2)))

if __name__ == '__main__':
    # zabbix = ZabbixAction("http://zabbix.meidai.f3322.net/zabbix", "Admin", "zabbix")
    # flag = zabbix.login()
    # host_list = []
    # if flag:
    #     host_list = zabbix.get_host()
    # else:
    # print("Not Login")
    # print("++++++")
    # print(type(host_list))

    # config = os.path.join(os.path.dirname(os.path.dirname(__file__)), "/adminset.conf")
    # mysql_config = get_config(config, 'zbmysql')
    # result = Cursor(mysql_config).get_one_result('hosts', ['host'])
    # print(result)

    # list1 = [{"ip": "127.0.0.1"}, {'ip': '10.10.10.233'}]
    # list2 = [{"ip": "127.0.0.1"}, {'ip': '10.10.10.234'}]
    #
    # list3 = []
    # list4 = []
    # for ip1 in list1:
    #     list3.append(ip1['ip'])
    #
    # for ip2 in list2:
    #     list4.append(ip2['ip'])
    #
    # diff = list(set(list4).difference(set(list3)))

    # before = [{'a': 1, 'b': 2}]
    # now = [{'a': 1, 'b': 3}]
    # lostlist = list(set(before.values()).difference(set(now.values())))
    # print lostlist

    # for k, v in ips:
    #     print(k, v)

    # config = os.path.join(os.path.dirname(os.path.dirname(__file__)), "./adminset.conf")
    # mysql_config = get_config(config)
    # print(mysql_config)

    # value = list(dict_diff()['ip'])
    # print(value, type(list(value)))

    # value = insert_ip()
    # print(value)
    # list_replace_dict()
    list_diff()