#!/bin/bash
set -e

# 安装依赖包
yum install -y epel-release
yum install -y gcc smartmontools dmidecode python-pip python-devel


echo "####install pip mirror####"
mkdir -p  ~/.pip
cat <<EOF > ~/.pip/pip.conf
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
EOF

echo "####client prepare finished!###"
