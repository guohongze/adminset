#!/bin/bash
set -e

cd "$( dirname "$0"  )"
cur_dir=$(pwd)

# 安装依赖包
os=$(cat /proc/version)
if (echo $os|grep centos) || (echo $os|grep 'Red Hat')
then
    yum install -y epel-release
    yum install -y gcc smartmontools dmidecode python-pip python-devel  libselinux-python dos2unix
elif (echo $os|grep Ubuntu)
then
    apt-get install smartmontools dmidecode python-pip python-dev tofrodos
    sed -i "s/PermitRootLogin/\#PermitRootLogin/g" /etc/ssh/sshd_config
    service ssh restart
else
    echo "your os version is not supported!"
fi


echo "####install pip mirror####"
mkdir -p  ~/.pip
cat <<EOF > ~/.pip/pip.conf
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
EOF

echo "####install pip packages####"
pip install --upgrade pip
pip install -U psutil==5.2.2
pip install -U schedule==0.4.3
pip install -U requests==2.11.1


echo "####config adminset agent####"
if (echo $os|grep centos) || (echo $os|grep 'Red Hat')
then
    scp $cur_dir/adminset_agent.py /usr/local/bin/
    scp $cur_dir/adminsetd.service /usr/lib/systemd/system/
    dos2unix /usr/local/bin/adminset_agent.py
    dos2unix /usr/lib/systemd/system/adminsetd.service
elif (echo $os|grep Ubuntu)
then
    scp $cur_dir/adminset_agent.py /usr/local/bin/
    scp $cur_dir/adminsetd.service /etc/systemd/system/
    fromdos /usr/local/bin/adminset_agent.py
    fromdos /etc/systemd/system/adminsetd.service
else
    echo "your os version is not supported!"
fi
echo "####client prepare finished!###"
service adminsetd start
service adminsetd restart
