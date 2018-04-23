#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:lvhaidong
# datetime:2018/4/20 13:55
# software: PyCharm

import urllib
import urllib2
import cookielib


class GraphDownload(object):
    def __init__(self):
        # post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）
        self.login_url = 'http://zabbix.meidai.f3322.net/zabbix/index.php'  # 从数据包中分析出，处理post请求的url
        self.graph_url = "http://zabbix.meidai.f3322.net/zabbix/chart2.php"

        # 设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

        # 构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                   'Referer': 'http://zabbix.meidai.f3322.net/zabbix/'}
        # 构造Post数据
        postData = {
            'name': 'Admin',  # 用户名
            'password': 'zabbix',  # 密码
            'autologin': 1,
            'enter': 'Sign in'
        }

        # 需要给Post数据编码
        postData = urllib.urlencode(postData)

        # 通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程
        request = urllib2.Request(self.login_url, postData, headers)
        response = urllib2.urlopen(request)
        # text = response.read()

    def get_graph(self, graphid, image_name):
        path = '/Users/lvhaidong/Desktop/main/static/zabbix/'  # 保存图片的地址
        values = {'width': 800, 'height': 200, 'graphid': graphid, 'stime': '20160907090409', 'period': 3600}
        data = urllib.urlencode(values)
        img_req = urllib2.Request(self.graph_url, data)
        png = urllib2.urlopen(img_req).read()
        file = path + image_name + '.png'
        with open(file, 'wb') as f:
            f.write(png)


if __name__ == '__main__':
    graph = GraphDownload()
    graph.get_graph('1095', "Mongodb")
