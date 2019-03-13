# AdminSet QuickStart
<img src="https://travis-ci.org/guohongze/adminset.svg?branch=master"></img> 
<img src="https://img.shields.io/hexpm/l/plug.svg"></img>
[![release](https://img.shields.io/github/release/guohongze/adminset.svg)](https://github.com/guohongze/adminset/releases)
<br>
Adminset基于DevOps理念开发，以整合全部运维场景为己任。Adminset是一个真正的基于运维思维而开发的全自动化运维平台。<br>

## v0.50 新功能
    全新用户权限系统
    基于用户角色的部署权限关联
    基于用户权限的功能按钮自动显示隐藏
    基于用户的WEBSSH授权
    django安全更新

## 开发环境
    centos 7.2(1511) django 1.11.16 python 2.7

## 服务端安装
    生产服务器建议 4核CPU，6G内存以上.
    学习测试建议 2核CPU，2G内存以上.
    服务器操作系统版本要求 centos7.2 centos7.4
    安装之前请关闭防火墙
```
git clone https://github.com/guohongze/adminset.git
adminset/install/server/auto_install.sh
```
说明：手动自定义安装请使用
adminset/install/server/server_install.sh


## 客户端安装
    客户端脚本目前rhel/centos6、centos7,ubuntu16.04
    客户端python版本支持2.6.6及以上
    说明：为保证注册IP是管理IP（后续会被ansible等调用），客户端的IP抓取目前使用主机名解析，否则报错。
    如：主机名为cn-bj-web01 请在/etc/hosts中加入相应的解析 192.168.x.x cn-bj-web01，这样再执行adminset_agent.py 可以保证正常运行。

step1: 修改文件install/client/adminset_agent.py :
```
客户端正常使用需要修改脚本中的两个字段：
token = 'HPcWR7l4NJNJ'        #token是上传到服务器的密钥可以在WEB界面的系统配置中自定义
server_ip = '192.168.47.130'  #此项目为adminset server的IP地址
```

step2: 拷贝install/client/ 目录到客户机的任意位置并执行:
```
cd client
/bin/bash install.sh
```
step3: 客户端管理
```
service adminsetd start|stop|restart|status
```
注意：客户端全部功能需要配置服务器到客户端的ssh免密登录。


## 访问
    关闭防火墙或开通80端口
    http://your_server_ip
    自动安装的用户名admin 密码Adminset123
    手动安装使用自定义创建的super admin用户名密码

## 说明
使用手册，<a href="http://115.28.147.154/static/docs/">使用手册</a><br>
FAQ参考，<a href="https://github.com/guohongze/adminset/wiki/FAQ">常见问题</a>

## demo
    每2小时重置一次数据
    http://115.28.147.154
    用户名admin 密码Adminset123

## 安全
    强烈建议您不要将程序对公网开放
    如果需要公网访问请使用VPN
    建议生产环境中使用https配置服务器，并对命令执行、webssh等模块进行安全强化
    由于开发方便，在django的settings中开启了DEBUG，在生产中需要关闭并指定自己的域名。

## 开发者交流
    请加入开发者群
    3号群 730232593


