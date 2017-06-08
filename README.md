# Adminset
<img src="https://travis-ci.org/guohongze/adminset.svg?branch=master"></img><br>
The open source operation platform : CMDB, project deploy, DevOps , Monitor. <br>
开源DevOps平台：资产管理、项目部署、自动运维、系统监控


## 服务端说明
#### step1:准备
建议将服务器端安装在centos7上，程序使用/opt/adminset目录（强制）<br>
cd /opt<br>
git clone https://github.com/guohongze/adminset.git<br>
执行安装脚本<br>
/opt/adminset/install/server_install.sh<br>

#### step2:运行
安装成功后自动运行,以下为启动管理方法<br>
service nginx {start|stop|restart}<br>
service adminset {start|stop|restart}<br>
service redis {start|stop|restart}<br>
service mariadb {start|stop|restart}<br>
/opt/adminset/install/celery_start.sh （重启后需要执行此文件，否则定时任务无法执行）<br>

#### step3:配置免密钥登陆客机(可选)
ssh-keygen<br>
ssh-copy-id -i /root/.ssh/id_rsa.pub {客户机IP}<br>
ansible和shell管理客户机需要此配置




## 客户端说明
说明：为保证注册IP是管理IP（后续会被ansible等调用），客户端的IP抓取目前使用主机名解析，也就是说主机名必须可以被解析才能执行自动上报脚本，否则报错。
如：主机名为centos6 请在/etc/hosts中加入相应的解析 192.168.x.x centos6，这样再执行agent_post_info.py 可以保证正常运行。
centos7不进行解析也可获取主机IP，但是centos6必须在/etc/hosts对主机名进行解析。
#### step1:
yum install -y smartmontools <br>
yum install -y dmidecode
#### step2:
在客户机上执行 scripts/agent_post_info.py 文件自动上报主机信息<br>
注意：执行前请编辑scripts/agent_post_info.py文件 保证 token 和server_url是正确的，token可以在服务端web界面系统配置中获得

## 访问
http://your_server_ip:8000<br>
使用自己在安装过程中创建的super admin用户名密码

# API
#### 获取主机信息
http://your_server_ip:8000/cmdb/get/host/?token=your_token&name=host_name <br>
#### 获取组信息
http://your_server_ip:8000/cmdb/get/group/?token=your_token&name=group_name <br>
http://your_server_ip:8000/cmdb/get/group/?token=your_token&name=all <br>
# dashboard
<img src="https://github.com/guohongze/adminset/blob/master/static/dist/img/demo.png"></img>
# 安全
建议不要将程序启动在有公网可以直接访问的设备上，如果需要请使用VPN。<br>
建议生产环境中使用https配置服务器<br>

# 定时任务用法
首先新建interval 或crontab<br>
新建任务填写名字<br>
选择间隔或crontab<br>
在Keyword arguments:处的写法是json格式：<br>
    执行命令<br>
    {"host":"c1", name:"service tomcat restart"}<br>
    执行脚本<br>
    {"host":"c1", name:"reboot.sh"}<br>
拉到最下边Task (registered)<br>
setup.tasks.command是直接向目标机器发送命令<br>
setup.tasks.scripts是在目标机器上执行一个你已经上传到服务器中的脚本<br>

