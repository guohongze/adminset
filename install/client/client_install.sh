#!/bin/bash
set -e

# 安装依赖包
os=$(cat /proc/version)
if (echo $os|grep centos) || (echo $os|grep 'Red Hat')
then
    yum install -y epel-release
    yum install -y gcc smartmontools dmidecode python-pip python-devel  libselinux-python
elif (echo $os|grep Ubuntu)
then
    apt-get install smartmontools dmidecode python-pip python-dev
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

echo "####client prepare finished!###"
