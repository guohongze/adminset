#!/bin/bash
#
set -e
cd "$( dirname "$0"  )"
cur_dir=$(pwd)
work_dir=/var/opt/adminset/client

# 获取用户输入的服务器地址和密钥
echo "####配置AdminSet客户端####"
echo "请输入AdminSet服务器的IP地址或域名 (默认: 192.168.110.100):"
read -r server_input
server_input=$(echo "$server_input" | xargs)  # 去除空格

echo "请输入AdminSet客户端认证密钥 (默认: HPcWR7l4NJNJ):"
read -r token_input
token_input=$(echo "$token_input" | xargs)  # 去除空格

# 如果用户没有输入，使用默认值
if [ -z "$server_input" ]; then
    server_input="192.168.110.100"
    echo "使用默认服务器地址: $server_input"
fi

if [ -z "$token_input" ]; then
    token_input="HPcWR7l4NJNJ"
    echo "使用默认密钥: $token_input"
fi

echo "注意: 客户端密钥必须与服务器端config设置中的密钥相同，否则会导致认证失败！"
echo "您现在可以在管理界面的系统配置中确认或修改密钥设置。"

# 修改adminset_agent.py中的服务器地址和密钥
if [ -f "$cur_dir/adminset_agent.py" ]; then
    # 备份原始文件
    cp "$cur_dir/adminset_agent.py" "$cur_dir/adminset_agent.py.bak"
    
    # 使用sed替换服务器地址和密钥
    sed -i "s/^token = .*$/token = '$token_input'/" "$cur_dir/adminset_agent.py"
    sed -i "s/^server_ip = .*$/server_ip = '$server_input'/" "$cur_dir/adminset_agent.py"
    
    echo "已更新服务器地址和密钥配置"
else
    echo "警告: 找不到adminset_agent.py文件，无法更新配置"
fi

# 检测Python版本
get_python_version() {
    python -c "import sys; print('%d.%d' % (sys.version_info[0], sys.version_info[1]))" 2>/dev/null || echo "0.0"
}

# 检测是否为新版Ubuntu (20.04+)
is_new_ubuntu() {
    if grep -q "Ubuntu" /etc/os-release; then
        ubuntu_version=$(grep -oP '(?<=VERSION_ID=").*?(?=")' /etc/os-release)
        if [ $(echo "$ubuntu_version >= 20.04" | bc) -eq 1 ]; then
            return 0
        fi
    fi
    return 1
}

# 检测是否为Ubuntu 24.04或更高版本
is_ubuntu_24_or_newer() {
    if grep -q "Ubuntu" /etc/os-release; then
        ubuntu_version=$(grep -oP '(?<=VERSION_ID=").*?(?=")' /etc/os-release)
        if [ $(echo "$ubuntu_version >= 24.04" | bc) -eq 1 ]; then
            return 0
        fi
    fi
    return 1
}

# 安装依赖包
os=$(cat /proc/version)
if (echo $os|grep centos) || (echo $os|grep 'Red Hat')
then
    yum makecache fast
    yum install -y epel-release
    yum install -y gcc smartmontools dmidecode python-pip python-devel libselinux-python dos2unix
elif (echo $os|grep Ubuntu)
then
    apt-get update
    # 检查是否为Ubuntu 24.04或更高版本 (PEP 668兼容性)
    if is_ubuntu_24_or_newer; then
        echo "####detected Ubuntu 24.04 or newer, using PEP 668 compatible installation####"
        apt-get install -y gcc smartmontools dmidecode python3-full python3-venv python3-pip tofrodos bc
        # 创建python链接指向python3，如果需要的话
        if [ ! -e /usr/bin/python ]; then
            ln -s /usr/bin/python3 /usr/bin/python
        fi
    # 检查是否为新版Ubuntu (20.04+)
    elif is_new_ubuntu; then
        echo "####detected Ubuntu 20.04 or newer, using Python 3####"
        apt-get install -y gcc smartmontools dmidecode python3-pip python3-dev tofrodos bc
        # 创建python链接指向python3，如果需要的话
        if [ ! -e /usr/bin/python ]; then
            ln -s /usr/bin/python3 /usr/bin/python
        fi
    else
        # 旧版Ubuntu使用原来的包
        apt-get install -y gcc smartmontools dmidecode python-pip python-dev tofrodos
    fi
    sed -i "s/PermitRootLogin/\#PermitRootLogin/g" /etc/ssh/sshd_config
    service ssh restart 2>/dev/null || systemctl restart ssh 2>/dev/null || echo "SSH service not restarted, please check manually"
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
mkdir -p $work_dir

source /etc/profile

echo "####config adminset agent####"
PYTHON_VERSION=$(get_python_version)

if (echo $os|grep centos) || (echo $os|grep 'Red Hat')
then
    if (echo $PYTHON_VERSION | grep -E "^2.6")
    then
        # Python 2.6 特殊处理
        pip install -U pip==9.0.3
        pip install virtualenv==14.0.0
        pip install setuptools==28.5.0
        scp $cur_dir/adminset_agent.py $work_dir
        scp $cur_dir/uninstall.sh $work_dir
        scp $cur_dir/adminsetd /etc/init.d/
        dos2unix $work_dir/adminset_agent.py
        dos2unix /etc/init.d/adminsetd
        chmod +x /etc/init.d/adminsetd
        chkconfig adminsetd on
    elif (echo $PYTHON_VERSION | grep -E "^2.7")
    then
        # Python 2.7 处理
        pip install -U pip==19.0.3
        pip install virtualenv==15.2.0
        scp $cur_dir/adminset_agent.py $work_dir
        scp $cur_dir/uninstall.sh $work_dir
        scp $cur_dir/adminsetd.service /usr/lib/systemd/system/
        dos2unix $work_dir/adminset_agent.py
        dos2unix /usr/lib/systemd/system/adminsetd.service
        systemctl daemon-reload
        systemctl enable adminsetd
    else
        # Python 3.x 处理
        pip3 install -U pip
        pip3 install virtualenv
        scp $cur_dir/adminset_agent.py $work_dir
        scp $cur_dir/uninstall.sh $work_dir
        scp $cur_dir/adminsetd.service /usr/lib/systemd/system/
        dos2unix $work_dir/adminset_agent.py
        dos2unix /usr/lib/systemd/system/adminsetd.service
        systemctl daemon-reload
        systemctl enable adminsetd
    fi
elif (echo $os|grep Ubuntu)
then
    # 复制必要文件
    cp $cur_dir/adminset_agent.py $work_dir
    cp $cur_dir/uninstall.sh $work_dir
    cp $cur_dir/adminsetd.service /etc/systemd/system/
    
    # 根据系统类型使用正确的工具处理文本文件
    if command -v fromdos &> /dev/null; then
        fromdos $work_dir/adminset_agent.py
        fromdos /etc/systemd/system/adminsetd.service
    elif command -v dos2unix &> /dev/null; then
        dos2unix $work_dir/adminset_agent.py
        dos2unix /etc/systemd/system/adminsetd.service
    fi
    
    systemctl daemon-reload
    systemctl enable adminsetd
else
    echo "your os version is not supported!"
fi

cd $work_dir

# 在Ubuntu 24.04及更高版本上使用python3 -m venv创建虚拟环境
if is_ubuntu_24_or_newer; then
    python3 -m venv venv
else
    # 对于其他系统继续使用virtualenv
    if is_new_ubuntu || (echo $PYTHON_VERSION | grep -E "^3"); then
        pip3 install -U pip
        pip3 install virtualenv
    elif (echo $PYTHON_VERSION | grep -E "^2.7"); then
        pip install -U pip==19.0.3
        pip install virtualenv==15.2.0
    fi
    virtualenv venv
fi

# 根据Python版本安装不同的依赖版本
source $work_dir/venv/bin/activate
if (echo $PYTHON_VERSION | grep -E "^2.6")
then
    # Python 2.6 兼容包
    pip install requests==2.11.1
    pip install psutil==5.2.2
    pip install schedule==0.4.3
    pip install simplejson==3.8.2
    pip install distro==1.0.4
elif (echo $PYTHON_VERSION | grep -E "^2.7")
then
    # Python 2.7 兼容包
    pip install requests==2.22.0
    pip install psutil==5.6.7
    pip install schedule==0.6.0
    pip install distro==1.4.0
else
    # Python 3.x 包
    pip install requests
    pip install psutil
    pip install schedule
    pip install distro
fi

echo "####client prepare finished!###"
if (echo $PYTHON_VERSION | grep -E "^2.6")
then
    service adminsetd start
else
    systemctl start adminsetd
fi
echo "####client install finished!###"
echo "服务器地址: $server_input"
echo "客户端密钥: $token_input"
echo "请确保这些设置与服务器端配置一致"
if (echo $PYTHON_VERSION | grep -E "^2.6")
then
    echo "please using <service adminsetd start|restart|stop> manage adminset agent"
else
    echo "please using <systemctl start|restart|stop adminsetd> manage adminset agent"
fi
