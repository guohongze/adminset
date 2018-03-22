#   Hostname 主机名
    adminset程序依赖主机名，所以被控机器、客户机，都需要设置主机名，主机名唯一，并且可以被解析
    请在 /etc/hosts 或是DNS中加入主机名的解析。

#   Install 安装部署 
    安装需要使用yum源请保证可用，或使用本地yum源。
    如果ubuntu客户端需要ansible等管理功能，需要开启root登录(配置脚本会自动开始，如不需要请手工关闭)

    一、服务器安装：
        1.1、下载代码
            git clone https://github.com/guohongze/adminset.git
        1.2、执行安装脚本-自动
            adminset/install/server/auto_install.sh
            如果使用自动安装则手动安装跳过,如果手动安装则跳过此步。
            访问：http://your_server_ip
            使用用户名admin 密码Adminset123
        1.3、执行安装脚本-手动
            1.3.1 adminset/install/server/server_install.sh
            安装过程需要输入管理员数据库等交互信息，如果安装中断再次执行server_install.sh即可.
            安装过程中会生成rsa密钥，位于/root/.ssh 目录下，如果已经存在，忽略即可。
            1.3.2、手动安装交互信息说明
            1）如果系统开启了selinux会提示：Do you want to disabled selinux?[yes/no]
               选择yes。(默认yes)
            2）YUM源选择提示do you want to use an internet yum repository?[yes/no]
               没有本地的yum源请选择yes，如果有本地的YUM源（包括epel源）请选择no。(默认值yes)
            3）数据库选择提示：do you want to create a new mysql database?[yes/no]
               本地没有数据库选择yes自动下载安装mariadb数据库，如已经存在mysql或mariadb数据库选择no，然后填写相关信息主机、端口、用户名、密码。(默认值yes)
            4）mongodb选择提示：do you want to create a new Mongodb?[YES/no]
               本地没有mongodb选择yes自动下载安装mongodb数据库，如已经存在mongodb数据库选择no，然后填写相关信息主机、端口、用户名、密码。(默认值yes)
            5）创建超管用户提示，please create your adminset' super admin: 输入超管用户名、邮件、密码。
            6）访问：
               http://your_server_ip
               使用自己在安装过程中创建的super admin用户名密码
    二、客户端安装
        说明：为保证注册IP是管理IP（后续会被ansible等调用），客户端的IP抓取目前使用主机名解析，否则报错。 如：主机名为cn-bj-web01 请在/etc/hosts中加入相应的解析 192.168.x.x cn-bj-web01，这样再执行adminset_agent.py 可以保证正常运行。 centos7不进行解析也可获取主机IP.
        step1:安装依赖
        拷贝adminset/install/client/client_install.sh 到客户机上并执行:
        sh client_install.sh

        step2:执行agent
        拷贝adminset/install/client/adminset_agent.py 到客户机上并执行：
        python adminset_agent.py
        后台运行请参考：
        nohup adminset_aent.py &
        agent默认每1800秒上传一次资产和硬件信息，可以在adminset_agent.py中自定义

    三、自动免密钥登陆
        如果实现全自动ssh免密登入客户机需要如下几个条件：
        1）客户机的所有密码都相同。
        2）在服务器的配置管理>密钥设置ssh password中写入客户机的密码并保存。
        3）这样当客户机第一次上报资产信息到服务器中去会自动触发ssh密钥分发，自动分发成功能后ansible等其它功能不需要手动再配置ssh免密登陆。

#   程序目录
    安装脚本会将文件安装在/var/opt/adminset
    main为程序代码
    config 配置
    pid pid文件
    logs 日志
    data 常用数据
    workspace 持续部署模块工作目录

#   站点导航用法
    在站点管理中输入常用的运维工具系统后会自动出现在站点导航界面。

#   资产管理用法
    一、资产管理
        表关系为主机管理关联IDC管理，每个主机选择一相对应的IDC。
        表关系为主机管理关联组管理，每个主机选择一相对应的组。
        组的作用在于任务编排模块的功能在调用组时的依据，比如ansible管理目标机器以组为单为时。
        组与主机的设置是一对多，意义是对于硬件组的管理，而非逻辑业务组。
        install/client/adminset_agent.py 开启后会自动上报主机相关信息到CMDB
        获取主机信息
        http://your_server_ip/cmdb/get/host/?token=your_token&name=host_name
        获取所有主机：
        http://your_server_ip/cmdb/get/host/?token=your_token&name=all
        获取组信息：
        http://your_server_ip/cmdb/get/group/?token=your_token&name=group_name
        获取所有组：
        http://your_server_ip/cmdb/get/group/?token=your_token&name=all

#    应用管理
     一、应用管理
        1.1 产品线，一个产品线包含多个项目，表关系为一对多。每个产品线或项目有负责人是多对一。
        1.2 项目管理
            1）源类型，必须与源地址对应，如源码服务器为gitlab选择git，svn选择svn
            2）源地址将会对持续交付产生影响，持续交付中的部署动作将会调用这些信息作为源文件的下载信息。
               支持svn svn协议 如 svn://svn.adminset.com/project
               支持svn http协议 如 http(s)://svn.adminset.com/project
               支持git ssh协议 如 git@gitlab.com/website/project.git 使用ssh协议时请确认相关密钥已经加入到git服务器相应账号中。
               支持git http协议 如 http(s)://github.com/website/project.git
               支持git http协议 如 http(s)://username@gitlab.com/website/project.git
            3）程序部署路径为程序部署在目标服务器的路径，程序将调用rsync做全量或增量同步。
               格式举例: /data/www/project
            4）配置文件路径功能暂时没有实装，留空白，或加上只相当于注释作用。
            5）所在服务器，部署的目标服务器，将会被持续交付模块的部署动作调用。
         1.3 认证管理
            此条目中保存所有系统中调用外部资源使用的用户权限信息，如下载私有gitlab repository的用户名
            与密码，此条目被持续交付中的部署任务所关联。如果部署任务需要外部权限则创建，然后调用。  
            
#   启用webssh
    需要设置域名解析，默认域名为adminset.cn（可以在配置管理页面进行变更）
    需要将这个域名做泛解析指向adminset所在的服务器，在本地或公网DNS都行，如果没有可以设置HOSTS解析，但HOSTS不支持泛解析。
    这样做是为了解决webssh启动时区分不同session进行认证而设置。

    指向完成后点击资产管理中的webssh按钮会触发域名格式如下：
    {{ host.hostname }}.adminset.cn:2222/ssh/host/{{ host.ip }}
    如主机名为cmdb IP为 192.168.47.130
    http://cmdb.adminset.cn:2222/ssh/host/192.168.47.130
    通过此URL进入webssh访问界面，第一次进入时会询问用户名密码，请填写系统对应的用户和密码即可。


#   定时任务用法
    首先新建interval 或crontab
    新建任务填写名字
    选择间隔或crontab
    在Keyword arguments(任务指令):处的写法是json格式：
        执行命令<br>
        {"host":"c1", name:"service tomcat restart"}
        执行脚本<br>
        {"host":"c1", name:"reboot.sh"}
    拉到最下边Task (registered)
    setup.tasks.command是直接向目标机器发送命令
    setup.tasks.scripts是在目标机器上执行一个你已经上传到服务器中的脚本，默认路径/var/opt/adminset/data/scripts
    注意：已经运行任务以后，再去修改任务不会立即生效，需要重启beat组件，在任务编排的后台管理中可以重启。
          这是由于celery的BUG导致，会在社区发布稳定版本以后修复。

#   ansible用法
    1、自动设置证书认证
    通过adminset_agent自动上报的服务器，可以自动设置免密登入(认书认证)
    前提是已经在客户端做了hosts解析，并且密码与在服务器的系统配置>密钥设置>ssh password
    相同，也就是说如果自动分发密钥必须在系统配置中提前输入密码并保存，系统默认带的密码是root。
    注意：系统只有在第一次上报信息时会调用ssh密钥分发.如果以后想使用自动密钥分发需要在资产管理中删除服务信息，然后再自动上报即可。

    2、手工设置认证书认证。
    配置免密钥登陆客机(ansible和shell管理客户机需要此配置)
    在服务器上执行
    ssh-keygen -q -N "" -t rsa -f /root/.ssh/id_rsa
    ssh-copy-id -i /root/.ssh/id_rsa.pub {客户机IP}
    输入客户机密码后认证成功可以ssh免密登入

    CMDB自动上报主机以后，在ansible页面执行"同步数据"按钮 将主机信息写入ansible的hosts文件
    然后将playbook 或是role脚本上传到/var/opt/adminset/data/playbook 或/var/opt/adminset/data/roles

#   shell用法
    依赖免密登入（与ansible同）
    CMDB自动上报主机以后，shell界面可以直接调用主机。
    然后将常用脚本上传到/var/opt/adminset/data/scripts 中shell脚本栏将会自动发现脚本。

#   持续交付用法
    依赖免密登入（与ansible同）
    持续交付模块具体作用为从源码服务器拉取代码到服务器本地，然后再通过rsync同步到project中指定的目标服务器中。持续交付的部署条目依赖应用管理模块中的项目，是一对一关系。
    1）部署策略，目前只支持直接部署一种模式。
    2）版本信息，可以不填写版本信息，默认将抓取默认分支
       源服务器为git时 写入git的tag名称 或是分支名如gitlab中的tag为1.8.0 则写入1.8.0，如果按分支发布则写相应分支名。
       源服务器为svn时 写入svn的tag或分支路径如： tags/v1.0 或 branches/br_dev01
    3）构建清理，勾选后将清除前一次拉取的代码，如果想增量下量代码时请不要勾选此项，不勾选此项将会使用git pull拉取运程代码。
    4）shell,代码发布后执行的shell，默认会在远程部署目标服务器上依次执行。
    5）本地执行，勾选后shell中的代码将在adminset所有服务器本地执行。
    6）认证信息，如果下载代码需要用户名密码等信息，在这些选择，此处调用应用管理中的认证管理。
    7）清理按钮不会终止部署任务，只会清理部署的状态，用于部署任务意外中止后任务卡进度条的情况。
    
#   监控平台用法
    当adminset_agent.py自动上报信息到，监控会自动发现并配置，无需干预.
    当监控页面打开时，前端JS每10秒会异步抓取监控数据
    agent默认每60秒上传一次监控数据，可以在adminset_agent.py中自定义

#   权限管理
    1、新建权限如：
    名字：资产管理
    URL：/cmdb/
    2、新建角色：
    名字：资产管理员
    可选择权限：资产管理
    3、新建用户
    在角色一栏选择：资产管理员


#   组件启动管理
    service adminset {start|stop|restart} # gunicorn管理程序
    service nginx {start|stop|restart}    # web server
    service redis {start|stop|restart}    # 缓存和任务列表
    service mariadb {start|stop|restart}  # 数据库，账号资产等信息
    service celery {start|stop|restart}   # 异步任务主程序
    service beat {start|stop|restart}     # 任务调用
    service mongod {start|stop|restart}   # 监控数据库
    service webssh {start|stop|restart}   # web终端功能

#   升级与更新
    强烈建设在升级或更新adminset之前先备份数据库，并在测试环境验证通过，因为adminset在快速的发展过程中，每版本功能与结构变化较大。
    1）版本更新：
        下载相应版本的代码到本地然后执行：
        chmdo +x adminset/install/server/update.sh
        adminset/install/server/update.sh
    2)二次开发
        rsync.sh脚本只做增量，rsync参数不带--delete选项，不会在生产环境删除代码中已删除的条目,不更新组件配置文件，不会生成新的ORM数据库条目。
        update.sh脚本带--delete选项，同步代码，重新发布各组件的配置文件，并重新生成ORM数据文件（makemigrations migrate）。
        update.sh 可带一个参数，参数为需要更新的应用名，如变更了appconf模块的models只更新appconf可以使用update.sh appconf来更新

# 安全
    强烈建议不要将程序启动在有公网可以直接访问的设备上，如果需要请使用VPN。
    建议生产环境中使用https配置服务器<br>
    建议adminset放在网管区中，并且开启防火墙。
    django的settings中开启了DEBUG，在生产中需要关闭并指定自己的域名。
    adminset设计初衷为超级管理员工具集成平台，所以后台权限都使用超管权限，如果生产环境中不符合安全要求，需要自定义各后台权限调用。

# 开发者交流
  QQ群：427794947
