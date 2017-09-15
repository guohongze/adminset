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
    read -p "Do you want to disabled selinux?[yes/no]": shut
    case $shut in
        yes|y|Y|YES)
            setenforce 0
            sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/sysconfig/selinux
            ;;
        no|n|N|NO)
            echo "please manual enable nginx access localhost 8000 port"
            echo "if not, when you open adminset web you will receive a 502 error!"
            sleep 3
            ;;
        *)
            exit 1
            ;;
    esac
fi


# 安装依赖
echo "####install depandencies####"
read -p "do you want to use an internet yum repository?[yes/no]:" yum1
if [ ! $yum1 ]
then
yum1=yes
fi
case $yum1 in
	yes|y|Y|YES)
	    yum install -y epel-release
		yum install -y gcc expect python-pip python-devel ansible smartmontools dmidecode libselinux-python
		;;
	no|n|N|NO)
        yum install -y gcc python-pip expect python-devel ansible smartmontools dmidecode libselinux-python
		;;
	*)
		exit 1
		;;
esac

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
read -p "do you want to create a new mysql database?[yes/no]:" db1
if [ ! $db1 ]
then
db1=yes
fi
case $db1 in
	yes|y|Y|YES)  
		echo "installing a new mariadb...."
		yum install -y mariadb-server mariadb-devel
		service mariadb start
		chkconfig mariadb on
		mysql -e "CREATE DATABASE if not exists adminset DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
		;;
	no|n|N|NO)
		read -p "your database ip address:" db_ip
		read -p "your database port:" db_port
		read -p "your database user:" db_user
		read -p "your database password:" db_password
		[ ! $db_password ] && echo "your db_password is empty confirm please press Enter key"
		[ -f /usr/bin/mysql ]
		sleep 3
		if [ $? -eq 0 ]
		then
			mysql -h$db_ip -P$db_port -u$db_user -p$db_password -e "CREATE DATABASE if not exists adminset DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
		else
			yum install -y mysql
			mysql -h$db_ip -P$db_port -u$db_user -p$db_password -e "CREATE DATABASE if not exists adminset DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
		fi
		sed -i "s/host = 127.0.0.1/host = $db_ip/g" $adminset_dir/adminset.conf
		sed -i "s/user = root/user = $db_user/g" $adminset_dir/adminset.conf
		sed -i "s/port = 3306/port = $db_port/g" $adminset_dir/adminset.conf
		sed -i "s/password =/password = $db_password/g" $adminset_dir/adminset.conf
		;;
	*) 
		exit 1                    
		;;
esac

# 安装mongodb
echo "####install mongodb####"
read -p "do you want to create a new Mongodb?[yes/no]:" mongo
if [ ! $mongo ]
then
mongo=yes
fi
case $mongo in
	yes|y|Y|YES)
		echo "installing a new Mongodb...."
		yum install -y mongodb mongodb-server
		/bin/systemctl start mongod 
		/bin/systemctl enable mongod 
		;;
	no|n|N|NO)
		read -p "your Mongodb ip address:" mongodb_ip
		read -p "your Mongodb port:" mongodb_port
		read -p "your Mongodb user:" mongodb_user
		read -p "your Mongodb password:" mongodb_pwd
		read -p "your Mongodb collection:" mongodb_collection
		[ ! $mongo_password ] && echo "your db_password is empty confirm please press Enter key"
		sleep 3
		sed -i "s/mongodb_ip = 127.0.0.1/host = $mongo_ip/g" $adminset_dir/adminset.conf
		sed -i "s/mongodb_user =/mongodb_user = $mongodb_user/g" $adminset_dir/adminset.conf
		sed -i "s/mongodb_port = 27017/port = $mongodb_port/g" $adminset_dir/adminset.conf
		sed -i "s/mongodb_pwd =/mongodb_pwd = $mongodb_pwd/g" $adminset_dir/adminset.conf
		sed -i "s/collection = sys_info/collection = $mongodb_collection/g" $adminset_dir/adminset.conf
		;;
	*)
		exit 1
		;;
esac

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
python manage.py createsuperuser
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
if [ -z ~/.ssh/id_rsa.pub ]
then
    ssh-keygen -q -N "" -t rsa -f /root/.ssh/id_rsa
else
    echo "you had already have a ssh rsa file."
fi
scp $adminset_dir/install/server/ssh/config ~/.ssh


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
