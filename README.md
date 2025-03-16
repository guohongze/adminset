# AdminSet 系统
![Build](https://img.shields.io/badge/Build-passing-green)
<img src="https://img.shields.io/badge/license-GPL-blue.svg"></img>
[![release](https://img.shields.io/github/release/guohongze/adminset.svg)](https://github.com/guohongze/adminset/releases)


## 项目概览

Adminset基于DevOps理念开发，以整合全部运维场景为己任。Adminset是一个真正的基于运维思维而开发的全自动化运维平台。

项目在中断七年后重启，Django框架从1.11.28升级到4.2.20，python从2.7升级到3.12，服务器从centos7升级到ubuntu24.04LTS。


## 服务端系统环境
  - Django 4.2.20 ✓ 
  - Ubuntu 24.04LTS ✓
  - Python 3.12 ✓
  - MariaDB 10.5+ ✓
  - Nginx 1.18+ ✓

## 安装指南

### 一键安装
为保证安装顺利，避免权限问题，安装时请切换到root身份(sudo -i)，而不是使用sudo。
我们提供了Ubuntu 24.04 LTS的自动化安装脚本，可以快速部署整个系统：

### 重复安装
项目的部署后路径为/var/opt/adminset 此目录下的main是主代码，其它为配置文件、临时文件、环境变量、上传文件等目录。在进行重新安装时auto_install.sh脚本会清空main目录和drop掉名为adminset的数据库，但会进行用户询问，不想清理输入n即可。

### 权限
部署过程会自动创建django admin账号，默认用户名和密码均为admin，部署完成后请及时修改密码。

```bash
# 克隆项目代码
git clone https://github.com/guohongze/adminset.git

# 进入安装目录
cd adminset/install

# 执行安装脚本（自动检测系统类型）
./server/auto_install.sh
```

安装过程中，系统会提示您输入访问AdminSet的域名，格式如`https://www.example.com`或`http://192.168.1.100`。这个域名将被添加到Django的CSRF信任列表中，以确保跨域请求的安全性。

如果您没有在安装过程中配置CSRF域名，或者需要添加更多域名，可以编辑`/var/opt/adminset/main/adminset/settings.py`文件，修改`CSRF_TRUSTED_ORIGINS`列表。


### 手动安装

如果您需要更精细地控制安装过程，可以参考以下步骤：

1. **安装基础环境**：
   ```bash
   # 在Ubuntu系统上
   apt update
   apt install -y build-essential python3-dev python3-pip libmariadb-dev libldap2-dev libsasl2-dev
   apt install -y mongodb-org redis-server
   ```

2. **创建虚拟环境**：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **安装依赖包**：
   ```bash
   pip install -r requirements.txt
   ```

4. **初始化数据库**：
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **启动服务**：
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## 客户端安装
客户端脚本支持rhel/centos7、Ubuntu系列
说明：为保证注册IP是管理IP（后续会被ansible等调用），客户端的IP抓取目前使用主机名解析，否则报错。
如：主机名为cn-bj-web01 请在/etc/hosts中加入相应的解析 192.168.x.x cn-bj-web01，这样再执行adminset_agent.py 可以保证正常运行。

step1: 拷贝install/client/ 目录到客户机的任意位置并执行:
```
cd client
/bin/bash install.sh
```

安装过程中，系统会提示您输入AdminSet服务器的IP地址或域名以及客户端认证密钥：
- 如果直接按回车，将使用默认值（默认服务器地址: 192.168.110.100，默认密钥: HPcWR7l4NJNJ）
- 请确保客户端密钥与服务器端config配置中的密钥相同，否则会导致认证失败

如果您需要手动修改这些设置，可以编辑`adminset_agent.py`文件：
```
token = 'HPcWR7l4NJNJ'        # token是上传到服务器的密钥，必须与服务器端config配置相同
server_ip = '192.168.47.130'  # 此项目为adminset server的IP地址或域名
```

step2: 客户端管理
```
service adminsetd start|stop|restart|status
```
或
```
systemctl start|stop|restart|status adminsetd
```

注意：客户端全部功能需要配置服务器到客户端的ssh免密登录。

## 主要功能模块

系统主要包含以下功能模块：

- **CMDB资产管理**：IT资产、设备和配置项的全生命周期管理
- **自动化配置**：自动化配置管理和应用部署
- **作业调度**：定时任务和批量作业管理
- **监控系统**：服务器性能和应用状态监控（使用MySQL存储监控数据）
- **工单系统**：IT服务请求和问题跟踪
- **webssh**：直接web免terminal登录
- **权限管理**：基于角色的访问控制

## 最新更改

- **监控数据存储**：监控数据现在支持使用MySQL存储，不再强依赖MongoDB
- **UI优化**：简化了用户界面，移除了不必要的按钮和功能入口
- **安全加固**：增强了系统安全性，减少了潜在的攻击面

## 访问
    关闭防火墙或开通80端口
    http://your_server_ip
    自动安装的用户名admin 密码admin
    手动安装使用自定义创建的super admin用户名密码


## **webssh功能**：
   - 为测试功能，严禁在公网使用。
   - webssh功能需要先配置应用管理中-认证中心-添加信息，保存用户名和密码，然后再从主机编辑中账号信息选择关联。
   - 如果不是超管用户，需要在role里进行授权才可使用webssh功能。

## **日志查看**：
   ```bash
   tail -f /var/opt/adminset/logs/adminset-error.log
   ```
   
   **服务状态**：
   ```bash
   systemctl status adminset.service
   systemctl status celery.service
   ```

## 安全
    强烈建议您不要将程序对公网开放
    如果需要公网访问请使用VPN
    建议生产环境中使用https配置服务器，并对命令执行等模块进行安全强化
    由于开发方便，在django的settings中开启了DEBUG，在生产中需要关闭并指定自己的域名。

## 说明
详细使用说明：自动化安装完成后打开 http://your_server_ip/static/docs/ <br>
FAQ参考，<a href="https://github.com/guohongze/adminset/wiki/FAQ">常见问题</a>
部署完成后，<a href="https://your_server_ip/static/docs/">详细使用说明</a>


