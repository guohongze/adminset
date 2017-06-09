#!/bin/bash
set -e
adminset_dir="/opt/adminset"
echo "####install depandencies####"
yum install -y epel-release
yum install -y make autoconf automake cmake gcc gcc-c++ 
yum install -y python python-pip python-setuptools python-devel openssl openssl-devel
yum install -y ansible smartmontools
mkdir -p /etc/ansible/scripts
mkdir -p /etc/ansible/playbook
echo "####install database####"
read -p "do you want to create a new mysql database?[yes/no]:" db1
case $db1 in
	yes|y|Y|YES)  
		echo "installing a new mariadb...."
		yum install -y mariadb-server mariadb-devel
		service mariadb start
		chkconfig mariadb on
		mysql -e "CREATE DATABASE adminset DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
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
			mysql -h$db_ip -P$db_port -u$db_user -p$db_password -e "CREATE DATABASE adminset DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
		else
			yum install -y mysql
			mysql -h$db_ip -P$db_port -u$db_user -p$db_password -e "CREATE DATABASE adminset DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
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
echo "####install adminset####"
yum install -y python-pip
mkdir -p  ~/.pip
cat <<EOF > ~/.pip/pip.conf
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
EOF
cd $adminset_dir
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
echo "please create your adminset' super admin:"
python manage.py createsuperuser
scp $adminset_dir/install/adminset.service /usr/lib/systemd/system
chkconfig adminset on
service adminset start
echo "####install redis####"
yum install redis -y
chkconfig redis on
service redis start
nohup celery -A adminset beat -l info -S django &
nohup celery -A adminset worker --loglevel=INFO --concurrency=10 -n work1@localhost &
echo "####install nginx####"
yum install nginx -y
chkconfig nginx on
scp $adminset_dir/install/adminset_nginx.conf /etc/nginx/conf.d
scp $adminset_dir/install/nginx.conf /etc/nginx
service nginx start
nginx -s reload
echo "##############install finished###################"
service mariadb start
service adminset start
echo "please access website http://server_ip"
echo "you have installed adminset successfully!!!"
echo "################################################"
