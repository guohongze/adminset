#!/bin/bash
set -e

# 初始化环境目录
main_dir="/var/opt/adminset"
adminset_dir="$main_dir/main"
data_dir="$main_dir/data"
config_dir="$main_dir/config"
logs_dir="$main_dir/logs"
cd "$( dirname "$0"  )"
cd .. && cd ..
cur_dir=$(pwd)
mkdir -p $adminset_dir
mkdir -p $data_dir/scripts
mkdir -p $data_dir/ansible/playbook
mkdir -p $data_dir/ansible/roles
mkdir -p $config_dir
mkdir -p $config_dir/webssh
mkdir -p $logs_dir
mkdir -p $main_dir/pid

# 关闭selinux
se_status=$(getenforce)
if [ $se_status != Enforcing ]
then
    echo "selinux is diabled, install progress is running"
    sleep 1
else
    echo "Please attention, Your system selinux is enforcing"
	setenforce 0
	sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/sysconfig/selinux
fi


# 安装依赖
echo "####install depandencies####"
yum install -y epel-release
yum install -y gcc expect python-pip python-devel ansible smartmontools dmidecode libselinux-python git rsync dos2unix

# build webssh
echo "build webssh"
/usr/bin/yum install -y nodejs
cd $cur_dir/vendor/WebSSH2
/usr/bin/npm install -g cnpm --registry=https://registry.npm.taobao.org
/usr/bin/cnpm install --production
/usr/bin/cnpm install forever -g

# 分发代码
if [ ! $cur_dir ] || [ ! $adminset_dir ]
then
    echo "install directory info error, please check your system environment program exit"
    exit 1
else
    rsync --delete --progress -ra --exclude '.git' $cur_dir/ $adminset_dir
fi
scp $adminset_dir/install/server/ansible/ansible.cfg /etc/ansible/ansible.cfg

# install webssh
scp /var/opt/adminset/main/install/server/webssh/webssh.service /usr/lib/systemd/system/webssh.service
systemctl enable webssh.service


#安装数据库
echo "####install database####"
echo "installing a new mariadb...."
yum install -y mariadb-server mariadb-devel
service mariadb start
chkconfig mariadb on
mysql -e "CREATE DATABASE if not exists adminset DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"


# 安装mongodb
echo "####install mongodb####"
echo "installing a new Mongodb...."
yum install -y mongodb mongodb-server
/bin/systemctl start mongod 
/bin/systemctl enable mongod 

# 安装主程序
echo "####install adminset####"
mkdir -p  ~/.pip
cat <<EOF > ~/.pip/pip.conf
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
EOF
pip install kombu==4.1.0
pip install celery==4.0.2
pip install billiard==3.5.0.3
pip install pytz==2017.2
pip install kombu==4.1.0
cd $adminset_dir/vendor/django-celery-results-master
python setup.py build
python setup.py install

cd $adminset_dir
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
echo "please create your adminset' super admin:"
#python manage.py createsuperuser
source /etc/profile
/usr/bin/mysql -e "insert into adminset.accounts_userinfo (password,username,email,is_active,is_superuser) values ('pbkdf2_sha256\$24000\$2odRjOCV1G1V\$SGJCqWf0Eqej6bjjxusAojWtZkz99vEJlDbQHUlavT4=','admin','admin@126.com',1,1);"
scp $adminset_dir/install/server/adminset.service /usr/lib/systemd/system
systemctl daemon-reload
chkconfig adminset on
service adminset start

#安装redis
echo "####install redis####"
yum install redis -y
chkconfig redis on
service redis start

# 安装celery
echo "####install celery####"
mkdir -p $config_dir/celery
scp $adminset_dir/install/server/celery/beat.conf $config_dir/celery/beat.conf
scp $adminset_dir/install/server/celery/celery.service /usr/lib/systemd/system
scp $adminset_dir/install/server/celery/start_celery.sh $config_dir/celery/start_celery.sh
scp $adminset_dir/install/server/celery/beat.service /usr/lib/systemd/system
chmod +x $config_dir/celery/start_celery.sh
systemctl daemon-reload
chkconfig celery on
chkconfig beat on
service celery start
service beat start

# 安装nginx
echo "####install nginx####"
yum install nginx -y
chkconfig nginx on
scp $adminset_dir/install/server/nginx/adminset.conf /etc/nginx/conf.d
scp $adminset_dir/install/server/nginx/nginx.conf /etc/nginx
service nginx start
nginx -s reload

# create ssh config
echo "create ssh-key, you could choose no if you had have ssh key"
if [ ! -e ~/.ssh/id_rsa.pub ]
then
    ssh-keygen -q -N "" -t rsa -f /root/.ssh/id_rsa
else
    echo "you had already have a ssh rsa file."
fi
scp $adminset_dir/install/server/ssh/config ~/.ssh/config


# 完成安装
echo "##############install finished###################"
systemctl daemon-reload
service redis restart
service mariadb restart
service adminset restart
service celery restart
service beat restart
service mongod restart
service sshd restart
service webssh restart
echo "please access website http://server_ip"
echo "you have installed adminset successfully!!!"
echo "################################################"
