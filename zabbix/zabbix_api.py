#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:lvhaidong
# datetime:2018/4/17 15:51
# software: PyCharm

import xlrd
import os
from pyzabbix import ZabbixAPI
import urllib
import urllib2
import cookielib


class ZabbixAction(object):
    #########################
    #    Global   Features  #
    #########################
    i = 0

    host_name_list = []
    host_id_list = []
    hostgroup_name_list = []
    hostgroup_id_list = []
    item_name_list = []
    item_id_list = []

    file_name = file

    # init
    def __init__(self, url, user, passwd):
        self.__url = url
        self.__user = user
        self.__password = passwd
        self.zapi = ZabbixAPI(self.__url)

    # 登录zabbix
    def login(self):
        try:
            self.zapi.login(self.__user, self.__password)
            return True
        except Exception, e:
            return False

    # 获取现zabbix中的所有主机
    def get_host(self):
        for i in self.zapi.host.get(output="extend"):
            self.host_name_list.append(str(i['name']))
        return self.host_name_list

    def get_hosts(self):
        hosts = self.zapi.host.get(output=['hostid', 'host'])
        return hosts

    def get_host_tem(self):
        data = {
            "output": ["hostid", "name"],
            "selectParentTemplates": ["templateid", "name"]
        }
        ret = self.zapi.host.get(**data)
        return ret

    def hostid_get_template(self, hostids):
        data = {
            "output": ["hostid"],
            "selectParentTemplates": ["templateid"],
            "hostids": hostids
        }
        return self.zapi.host.get(**data)

    def link_template(self, hostid, templateids):
        data = {
            "hostid": hostid,
            "templates": templateids
        }
        ret = self.zapi.host.update(data)
        return ret

    def unlink_template(self, hostid, templateid):
        return self.zapi.host.update(hostid=hostid, templates_clear=[{"templateid": templateid}])

    def get_template(self):
        ret = self.zapi.template.get(output=["templateid", "name"])
        return ret

    # 获取现zabbix中的所有主机组
    def get_hostgroup(self):
        return self.zapi.hostgroup.get(output=['groupid', 'name'])

    # 获取现zabbix中的每个主机的所有item
    def get_host_item_id(self, hostids):
        for i in self.zapi.item.get(hostids=hostids, output="extend"):
            self.item_name_list.append(str(i["name"]))
            self.item_id_list.append(str(i["itemid"]))
        all_item = dict(zip(self.item_id_list, self.item_name_list))
        return all_item

    #### 获取现zabbix中的每个主机的所有item
    def get_host_history(self, itemids, limit):
        data = {
            "output": "extend",
            "history": 0,
            "itemids": itemids,
            "limit": limit,
            "sortfield": "clock",
            "sortorder": "DESC",
        }
        ret = self.zapi.history.get(**data)
        print ret
        return ret

    #########################
    #    ZabbixAdd   Host   #
    #########################
    # 通过模板名获取模板ID
    def get_templateid(self, template_name):
        template_data = {
            "host": [template_name]
        }
        result = self.zapi.template.get(filter=template_data)
        if result:
            return result[0]['templateid']
        else:
            return result

    # 通过组名获取组ID
    def get_groupid(self, group_name):
        group_data = {
            "name": [group_name]
        }
        return str(self.zapi.hostgroup.get(filter=group_data)[0]['groupid'])

    # 打开xls文件
    def open_excel(self, file=file_name):
        try:
            data = xlrd.open_workbook(file)
            return data
        except Exception, e:
            print str(e)

    #### 将xls文件内主机导入到list
    def create_hosts(self, file):
        self.get_host()
        data = self.open_excel(file)
        # print data.sheets()[0]
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        list = []
        for rownum in range(1, nrows):
            list.append(table.row_values(rownum))
        fo = open('/tmp/cache_add_zabbix.txt', 'w')
        for host in list:
            host_name = host[0]
            visible_name = host[1]
            host_ip = host[2]
            group = host[3]
            groupid = self.get_groupid(group)
            template = host[4]
            templateid = self.get_templateid(host[4])
            inventory_location = host[5]

            host_data = {
                "host": host_name,
                "name": visible_name,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": host_ip.strip(),
                        "dns": "",
                        "port": "10050"
                    }
                ],
                "groups": [
                    {
                        "groupid": groupid
                    }
                ],
                "templates": [
                    {
                        "templateid": templateid
                    }
                ],
                "inventory": {
                    "location": inventory_location
                }
            }

            # Create Host
            if host_data['name'] in self.host_name_list:
                s1 = ("❌ 主机: %s 已存在 请核实.!") % str(host_data["name"])
                fo.write(s1)
            else:
                self.zapi.host.create(host_data)
                s2 = ("✔️ 添加主机: %s 成功.!") % str(host_data["name"])
                fo.write(s2)
        fo.close()

    #########################
    #    ZabbixDelete  Host #
    #########################

    #### 删除主机
    def delete_host(self, server_list):
        fo = open('/tmp/cache_delete_zabbix.txt', 'w')
        res = []
        id = []

        [res.append(i.replace(' ', '')) for i in server_list]
        # print res

        for host_name in res:
            # print host_name
            if host_name not in self.get_host().keys():
                s1 = ("❌ 主机 %s 不存在或已删除,请核实.!") % str(host_name)
                print ("❌ 主机 %s 不存在或已删除,请核实.!") % str(host_name)
                fo.write(s1)
                # return  u"\033[1;31m 主机 %s 不存在或已删除,请核实！\033[0m" % host_name
            else:
                data = {"name": [host_name]}
                for host_id in str(self.zapi.host.get(filter=data)[0]['hostid']).split('\n'):
                    s2 = ("✔️ 主机:  %s ID: %s 删除成功.!") % (str(host_name), str(host_id))
                    print ("✔️ 主机:  %s ID: %s 删除成功.!") % (str(host_name), str(host_id))
                    fo.write(s2)
                    # return u"\033[1;32m 主机:  %s   ID: %s 删除成功！\033[0m" % (host_name,host_id)
                    id.append(host_id)
                    self.zapi.host.delete(host_id)
        fo.close()

    #########################
    #    GetZabbix  Data    #
    #########################

    # 获取特别指定主机的id，通过传入主机名
    def get_each_host(self, hostname):
        data = {
            "output": "extend",
            "filter": {"name": hostname}
        }
        print hostname
        for i in self.zapi.host.get(**data):
            return i['hostid']

    # 获取特定主机的组名称
    def get_each_groupname(self, hostname):
        data = {
            "output": "extend",
            "filter": {"name": hostname}
        }
        # print hostname
        res = self.zapi.host.get(**data)

        print res

    # 获取指定主机的graph_name对应的graph_id
    def get_graph(self, hostid, graph_name):
        data = {
            "output": "extend",
            "hostids": hostid,
            "sortfield": "name",
            "search": graph_name
        }
        ret = self.zapi.graph.get(**data)
        return ret

    # 获取主机对应的graph_id
    def get_graphid(self, hostid):
        data = {
            "output": ["graphid", "name"],
            "selectGraphs": ["graphid", "name"],
            "filter": {"hostid": hostid}
        }
        ret = self.zapi.host.get(**data)
        return ret[0]['graphs']

    # 通过组id获取相关组内的所有主机
    def get_hostingroup(self, groupid):
        data = {
            "output": ["groupid", 'name'],
            "groupids": groupid
        }
        host_list = []
        ret = self.zapi.host.get(**data)
        for i in ret:
            host_list.append(i['name'])
        return host_list

    # 通过特定主机名获取主机对应的主机组
    def get_host_groupname(self, hostname):
        data = {
            "output": ['groupid', 'name'],
            "filter": "name"
        }
        group_id = []
        group_name = []

        for i in self.zapi.hostgroup.get(**data):
            group_name.append(str(i['name']))
            group_id.append(str(i['groupid']))
        res = dict(zip(group_name, group_id))
        for k, v in res.items():
            for host_name in self.get_hostingroup(v):
                if host_name == hostname:
                    return k

    def create_host(self, params):
        return self.zapi.host.create(**params)

    def create_zabbix_host(self, hostid, groupid, url, user, password):
        ret = []
        for host in hostid:
            data = {
                "host": host,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": host,
                        "dns": "",
                        "port": "10050"
                    }
                ],
                "groups": [
                    {
                        "groupid": groupid
                    }
                ]
            }
            zabbix = ZabbixAction(url, user, password)
            flag = zabbix.login()
            if flag:
                ret.append(zabbix.create_host(data))
            else:
                ret.append("Not Login!")
        return ret


class GraphDownload(object):
    def __init__(self, login_url, graph_url):
        self.index_url = login_url
        self.graph_url = graph_url
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                   'Referer': 'http://zabbix.meidai.f3322.net/zabbix/'}
        postData = {
            'name': 'Admin',
            'password': 'zabbix',
            'autologin': 1,
            'enter': 'Sign in'
        }
        postData = urllib.urlencode(postData)
        request = urllib2.Request(self.index_url, postData, headers)
        response = urllib2.urlopen(request)
        # text = response.read()

    def get_graph(self, graphid, stime, image_dir="/tmp"):
        values = {'width': 800, 'height': 200, 'graphid': graphid, 'stime': stime, 'period': 3600}
        data = urllib.urlencode(values)
        img_req = urllib2.Request(self.graph_url, data)
        png = urllib2.urlopen(img_req).read()
        # image = image_dir + "/" + image_name + '.png'
        image = "%s/%s_%s.jpg" % (image_dir, values["graphid"], values["stime"])
        with open(image, 'wb') as f:
            f.write(png)
        return '1'


#     # # zabbix退出
#     # def zabbix_logout(token):
#     #     try:
#     #         data = json.dumps(
#     #             {
#     #                 "jsonrpc": "2.0",
#     #                 "method": "user.logout",
#     #                 "params": [],
#     #                 "id": 0,
#     #                 "auth": token
#     #             })
#     #         request_data = requests.post(zabbix_url, data=data, headers=headers)
#     #         result = json.loads(request_data.text)['result']
#     #         if result:
#     #             return "ok"
#     #         else:
#     #             log("登出失败，原因：%s" % e)
#     #             return "error"
#     #     except BaseException, e:
#     #         log("zabbix_logout: %s" % e)
#     #         return "error"
#     #
#     # # 获取主机组id
#     # def get_group_id(group_name):
#     #     try:
#     #         token = zabbix_login()
#     #         data = json.dumps(
#     #             {
#     #                 "jsonrpc": "2.0",
#     #                 "method": "hostgroup.get",
#     #                 "params": {
#     #                     "output": "extend",
#     #                     "filter": {
#     #                         "name": [
#     #                             group_name
#     #                         ]
#     #                     }
#     #                 },
#     #                 "auth": token,
#     #                 "id": 0
#     #             })
#     #         request = requests.post(zabbix_url, data=data, headers=headers)
#     #         group_id = json.loads(request.text)['result']
#     #         if len(group_id) == 0:
#     #             return "null"
#     #         else:
#     #             return group_id[0]['groupid']
#     #     except BaseException, e:
#     #         log("get_group_id: %s" % e)
#     #         return "error"
#     #     finally:
#     #         zabbix_logout(token)
#     #
#     # # 创建服务器组
#     # def create_group(group_name):
#     #     try:
#     #         token = zabbix_login()
#     #         data = json.dumps(
#     #             {
#     #                 "jsonrpc": "2.0",
#     #                 "method": "hostgroup.create",
#     #                 "params": {
#     #                     "name": group_name
#     #                 },
#     #                 "auth": token,
#     #                 "id": 0
#     #             })
#     #         request = requests.post(zabbix_url, data=data, headers=headers)
#     #         group_id = json.loads(request.text)['result']['groupids'][0]
#     #         return group_id
#     #     except BaseException, e:
#     #         log("create_group: %s" % e)
#     #         return "error"
#     #     finally:
#     #         zabbix_logout(token)
#     #
#     # # 获取模板id
#     # def get_template_id(template_name):
#     #     try:
#     #         token = zabbix_login()
#     #         data = json.dumps(
#     #             {
#     #                 "jsonrpc": "2.0",
#     #                 "method": "template.get",
#     #                 "params": {
#     #                     "output": "extend",
#     #                     "filter": {
#     #                         "host": [
#     #                             template_name
#     #                         ]
#     #                     }
#     #                 },
#     #                 "auth": token,
#     #                 "id": 0
#     #             })
#     #         request = requests.post(zabbix_url, data=data, headers=headers)
#     #         template_id = json.loads(request.text)['result'][0]['templateid']
#     #         return template_id
#     #     except BaseException, e:
#     #         log('get_template_id: %s' % e)
#     #         return "error"
#     #     finally:
#     #         zabbix_logout(token)
#     #
#     # # 创建主机
#     # def create_host(host_name, group_name, host_ip, host_port, template_name):
#     #     try:
#     #         token = zabbix_login()
#     #         template_id = get_template_id(template_name)
#     #         if template_id == "error":
#     #             return "error"
#     #         group_id = get_group_id(group_name)
#     #         if group_id == "error":
#     #             return "error"
#     #         data = json.dumps(
#     #             {
#     #                 "jsonrpc": "2.0",
#     #                 "method": "host.create",
#     #                 "params": {
#     #                     "host": host_name,
#     #                     "interfaces": [
#     #                         {
#     #                             "type": 1,
#     #                             "main": 1,
#     #                             "useip": 1,
#     #                             "ip": host_ip,
#     #                             "dns": "",
#     #                             "port": host_port
#     #                         }
#     #                     ],
#     #                     "groups": [
#     #                         {
#     #                             "groupid": group_id
#     #                         }
#     #                     ],
#     #                     "templates": [
#     #                         {
#     #                             "templateid": template_id
#     #                         }
#     #                     ],
#     #                 },
#     #                 "auth": token,
#     #                 "id": 0
#     #             })
#     #         request = requests.post(zabbix_url, data=data, headers=headers)
#     #         host_id = json.loads(request.text)['result']['hostids'][0]
#     #         return host_id
#     #     except BaseException, e:
#     #         log('create_host: %s' % e)
#     #         return "error"
#     #     finally:
#     #         zabbix_logout(token)
#     #
#     # # 删除主机
#     # def delete_host(host_id):
#     #     try:
#     #         token = zabbix_login()
#     #         data = json.dumps(
#     #             {
#     #                 "jsonrpc": "2.0",
#     #                 "method": "host.delete",
#     #                 "params": [
#     #                     host_id
#     #                 ],
#     #                 "auth": token,
#     #                 "id": 0
#     #             })
#     #         request = requests.post(zabbix_url, data=data, headers=headers)
#     #         host_id_deleted = json.loads(request.text)['result']['hostids'][0]
#     #         if host_id_deleted == host_id:
#     #             return "ok"
#     #         else:
#     #             log('delete_host: failed %s' % request.text)
#     #             return "failed"
#     #     except BaseException, e:
#     #         log('delete_host: %s' % e)
#     #         return "error"
#     #
#     # # 获取主机状态（监控状态是否正常）
#     # def get_host_status(hostid):
#     #     try:
#     #         token = zabbix_login()
#     #         data = json.dumps(
#     #             {
#     #                 "jsonrpc": "2.0",
#     #                 "method": "host.get",
#     #                 "params": {
#     #                     "output": ["available"],
#     #                     "hostids": hostid
#     #                 },
#     #                 "id": 0,
#     #                 "auth": token
#     #             })
#     #         request = requests.post(zabbix_url, data=data, headers=headers)
#     #         host_status = json.loads(request.text)['result'][0]['available']
#     #         if host_status == '1':
#     #             return "available"
#     #         else:
#     #             return "unavailable"
#     #     except BaseException, e:
#     #         log('get_host_status: %s' % e)
#     #         return "error"
#     #     finally:
#     #         zabbix_logout(token)
#     #
#     # # 根据监控名获取监控项最新值
#     # def get_item_value_name(host_id, item_name):
#     #     try:
#     #         token = zabbix_login()
#     #         data = json.dumps(
#     #             {
#     #                 "jsonrpc": "2.0",
#     #                 "method": "item.get",
#     #                 "params": {
#     #                     "output": "extend",
#     #                     "hostids": host_id,
#     #                     "search": {
#     #                         "name": item_name
#     #                     },
#     #                 },
#     #                 "auth": token,
#     #                 "id": 0
#     #             })
#     #         request = requests.post(zabbix_url, data=data, headers=headers)
#     #         last_value = json.loads(request.text)['result'][0]['lastvalue']
#     #         return last_value
#     #     except BaseException, e:
#     #         log('get_item_value_name: %s' % e)
#     #         return "error"
#     #     finally:
#     #         zabbix_logout(token)
#     #
#     # # 根据监控项键值获取监控项最新值
#     # def get_item_value_key(host_id, item_name):
#     #     try:
#     #         token = zabbix_login()
#     #         data = json.dumps(
#     #             {
#     #                 "jsonrpc": "2.0",
#     #                 "method": "item.get",
#     #                 "params": {
#     #                     "output": "extend",
#     #                     "hostids": host_id,
#     #                     "search": {
#     #                         "key_": item_name
#     #                     },
#     #                 },
#     #                 "auth": token,
#     #                 "id": 0
#     #             })
#     #         request = requests.post(zabbix_url, data=data, headers=headers)
#     #         last_value = json.loads(request.text)['result'][0]['lastvalue']
#     #         return last_value
#     #     except BaseException, e:
#     #         log('get_item_value_key: %s' % e)
#     #         return "error"
#     #     finally:
#     #         zabbix_logout(token)
#     #
#     # # 获取某个主机组下所有主机id
#     # def get_group_hosts_id(group_name):
#     #     try:
#     #         token = zabbix_login()
#     #         data = json.dumps(
#     #             {
#     #                 "jsonrpc": "2.0",
#     #                 "method": "hostgroup.get",
#     #                 "params": {
#     #                     "selectHosts": "hostid",
#     #                     "filter": {
#     #                         "name": [
#     #                             group_name
#     #                         ]
#     #                     }
#     #                 },
#     #                 "auth": token,
#     #                 "id": 0
#     #             })
#     #         request = requests.post(zabbix_url, data=data, headers=headers)
#     #         hosts = json.loads(request.text)['result'][0]['hosts']
#     #         host_id_list = []
#     #         for host_id in hosts:
#     #             host_id_list.append(host_id)
#     #         return host_id_list
#     #     except BaseException, e:
#     #         log('get_group_hosts_id %s' % e)
#     #         return "error"
#     #     finally:
#     #         zabbix_logout(token)
#     #
#     # # 获取主机的监控项数
#     # def get_host_item_num(host_id):
#     #     try:
#     #         token = zabbix_login()
#     #         data = json.dumps(
#     #             {
#     #                 "jsonrpc": "2.0",
#     #                 "method": "item.get",
#     #                 "params": {
#     #                     "hostids": host_id,
#     #                     "countOutput": "true",
#     #                 },
#     #                 "auth": token,
#     #                 "id": 0
#     #             })
#     #         request = requests.post(zabbix_url, data=data, headers=headers)
#     #         item_num = json.loads(request.text)['result']
#     #         return item_num
#     #     except BaseException, e:
#     #         log('get_item_num: %s' % e)
#     #         return "error"
#     #     finally:
#     #         zabbix_logout(token)
#     #
#     # # 获取主机的自发现规则id列表
#     # def get_LLD_ids(host_id):
#     #     try:
#     #         token = zabbix_login()
#     #         data = json.dumps(
#     #             {
#     #                 "jsonrpc": "2.0",
#     #                 "method": "discoveryrule.get",
#     #                 "params": {
#     #                     "output": "extend",
#     #                     "hostids": host_id
#     #                 },
#     #                 "auth": token,
#     #                 "id": 0
#     #             })
#     #         request = requests.post(zabbix_url, data=data, headers=headers)
#     #         item_ids = json.loads(request.text)['result']
#     #         lld_id_list = []
#     #         for item_id in item_ids:
#     #             lld_id_list.append(item_id['itemid'])
#     #         return lld_id_list
#     #     except BaseException, e:
#     #         log('get_LLD_ids: %s' % e)
#     #         return "error"
#     #     finally:
#     #         zabbix_logout(token)
#     #
#     # # 开启某个主机的自发现规则
#     # def LLD_on(item_id, host_id):
#     #     try:
#     #         token = zabbix_login()
#     #         data = json.dumps(
#     #             {
#     #                 "jsonrpc": "2.0",
#     #                 "method": "discoveryrule.update",
#     #                 "params": {
#     #                     "itemid": item_id,
#     #                     "hostids": host_id,
#     #                     "status": 0
#     #                 },
#     #                 "auth": token,
#     #                 "id": 0
#     #             })
#     #         request = requests.post(zabbix_url, data=data, headers=headers)
#     #         item_result = json.loads(request.text)['result']['itemids']
#     #         if len(item_result) != 0:
#     #             return "ok"
#     #         else:
#     #             return "failed"
#     #     except BaseException, e:
#     #         log('LLD_on: %s' % e)
#     #         return "error"
#     #     finally:
#     #         zabbix_logout(token)
#     #
#     # # 关闭某个主机的自发现规则
#     # def LLD_off(item_id, host_id):
#     #     try:
#     #         token = zabbix_login()
#     #         data = json.dumps(
#     #             {
#     #                 "jsonrpc": "2.0",
#     #                 "method": "discoveryrule.update",
#     #                 "params": {
#     #                     "itemid": item_id,
#     #                     "hostids": host_id,
#     #                     "status": 1
#     #                 },
#     #                 "auth": token,
#     #                 "id": 0
#     #             })
#     #         request = requests.post(zabbix_url, data=data, headers=headers)
#     #         lld_result = json.loads(request.text)['result']['itemids']
#     #         if len(lld_result) != 0:
#     #             return "ok"
#     #         else:
#     #             return "failed"
#     #     except BaseException, e:
#     #         log('LLD_off: %s' % e)
#     #         return "error"
#     #     finally:
#     #         zabbix_logout(token)
