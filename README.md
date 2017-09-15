# AdminSet
<img src="https://travis-ci.org/guohongze/adminset.svg?branch=master"></img> 
<img src="https://img.shields.io/hexpm/l/plug.svg"></img>
[![release](https://img.shields.io/github/release/guohongze/adminset.svg)](https://github.com/guohongze/adminset/releases)
<br>
Adminset基于DevOps理念开发，以整合全部运维场景为己任。Adminset是一个真正的基于运维思维而开发的全自动化运维平台。<br>

## v0.7 新功能
基于ssh2的 WEB terminal

## 开发环境
centos 7.2(1511) django 1.9.8（兼容Django1.11） python 2.7<br>

## 服务端安装
生产服务器建议 4核CPU，8G内存以上.<br>
学习测试建议 2核CPU，2G内存以上.<br>
服务器操作系统版本要求 centos7.2及以上<br>
安装过程需要输入管理员数据库等交互信息<br>
```
git clone https://github.com/guohongze/adminset.git
adminset/install/server/server_install.sh
```

## 客户端安装
客户端脚本目前rhel/centos6、7,ubuntu14.04经过测试<br>
客户端python版本支持2.6.6及以上<br>
说明：为保证注册IP是管理IP（后续会被ansible等调用），客户端的IP抓取目前使用主机名解析，否则报错。 
如：主机名为cn-bj-web01 请在/etc/hosts中加入相应的解析 192.168.x.x cn-bj-web01，这样再执行adminset_agent.py 可以保证正常运行。
#### step1:
拷贝install/client/client_install.sh 到客户机上并执行:
```
install/client/client_install.sh
```
#### step2:
拷贝install/client/adminset_agent.py 到客户机上并执行:
```
python adminset_agent.py
```
后台运行请参考：
```
nohup adminset_agent.py &
```

## 访问
http://your_server_ip<br>
使用自己在安装过程中创建的super admin用户名密码

## 说明
使用请转到，<a href="https://github.com/guohongze/adminset/blob/master/docs/Manual.txt">使用说明</a><br>
功能请转到，<a href="https://github.com/guohongze/adminset/wiki/AdminSet">功能说明</a><br>
FAQ请转到，<a href="https://github.com/guohongze/adminset/wiki/FAQ">常见问题</a>

# 安全
建议不要将程序启动在有公网可以直接访问的设备上，如果需要请使用VPN。<br>
建议生产环境中使用https配置服务器<br>
由于开发方便，在django的settings中开启了DEBUG，在生产中需要关闭并指定自己的域名。

# 开发者交流
请加入开发者群，注明来自github
<img src="https://github.com/guohongze/adminset/blob/master/static/dist/img/qq.png"></img>
