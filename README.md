# Adminset
<img src="https://travis-ci.org/guohongze/adminset.svg?branch=master"></img><br>
The open source operation platform : CMDB, project deploy, DevOps , Monitor. <br>
开源DevOps平台：资产管理、项目部署、自动运维、系统监控


## 服务端说明
建议将服务器端安装在centos7上，程序使用/opt/adminset目录（强制）<br>
cd /opt<br>
git clone https://github.com/guohongze/adminset.git<br>
执行安装脚本<br>
/opt/adminset/install/server_install.sh<br>



## 客户端说明
说明：为保证注册IP是管理IP（后续会被ansible等调用），客户端的IP抓取目前使用主机名解析，也就是说主机名必须可以被解析才能执行自动上报脚本，否则报错。
如：主机名为centos6 请在/etc/hosts中加入相应的解析 192.168.x.x centos6，这样再执行agent_post_info.py 可以保证正常运行。
centos7不进行解析也可获取主机IP，但是centos6必须在/etc/hosts对主机名进行解析。
#### step1:
yum install -y smartmontools <br>
yum install -y dmidecode
#### step2:
在客户机上执行 scripts/agent_post_info.py 文件自动上报主机信息<br>

## 访问
http://your_server_ip<br>
使用自己在安装过程中创建的super admin用户名密码

## 使用说明
平台说明用说明请转到：<a href="https://github.com/guohongze/adminset/blob/master/docs/Manual.txt">使用说明</a>
# dashboard
<img src="https://github.com/guohongze/adminset/blob/master/static/dist/img/asset.png"></img>
# 安全
建议不要将程序启动在有公网可以直接访问的设备上，如果需要请使用VPN。<br>
建议生产环境中使用https配置服务器<br>



