# Adminset
<img src="https://travis-ci.org/guohongze/adminset.svg?branch=master"></img> 
<img src="https://img.shields.io/hexpm/l/plug.svg"></img>
<br>
adminset基于DevOps理念开发，以整合全部运维场景为己任<br>
自动上报注册主机，自动ansible关联，监控自动发现<br>
adminset是一个真正的基于运维思维而开发的全自动化运维平台。<br>

## v0.3.0 新功能
新增监控平台模块<br>
监控内容自动发现<br>
agent重构，自动多线程上报<br>

## 开发环境
centos 7.2(1511) django 1.9.8 python 2.7<br>

## 服务端安装
推荐服务器配置 4核CPU，8G内存.<br>
测试最低要求 2核CPU，4G内存.<br>
服务器操作系统版本要求 centos7.2及以上<br>
git clone https://github.com/guohongze/adminset.git<br>
执行安装脚本<br>
adminset/install/server_install.sh<br>
安装过程需要输入管理员数据库等交互信息<br>


## 客户端安装
客户端脚本在centos上开发，目前支持6和7，在ubuntu等其它平台可能会需要做部分兼容性修定<br>
说明：为保证注册IP是管理IP（后续会被ansible等调用），客户端的IP抓取目前使用主机名解析，否则报错。 如：主机名为cn-bj-web01 请在/etc/hosts中加入相应的解析 192.168.x.x cn-bj-web01，这样再执行adminset_agent.py 可以保证正常运行。 centos7不进行解析也可获取主机IP.
#### step1:
yum install -y smartmontools dmidecode python-pip
#### step2:
拷贝client/adminset_agent.py 到客户机上并执行，自动上报主机信息.
后台运行请参考：
nohup adminset_agent.py &

## 访问
http://your_server_ip<br>
使用自己在安装过程中创建的super admin用户名密码

## 使用说明
请转到：<a href="https://github.com/guohongze/adminset/blob/master/docs/Manual.txt">使用说明</a>
# dashboard
<img src="https://github.com/guohongze/adminset/blob/master/static/dist/img/asset.png"></img>
# 安全
建议不要将程序启动在有公网可以直接访问的设备上，如果需要请使用VPN。<br>
建议生产环境中使用https配置服务器<br>
由于开发方便，在django的settings中开启了DEBUG，在生产中需要关闭并指定自己的域名。


