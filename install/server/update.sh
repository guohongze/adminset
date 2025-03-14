#!/bin/bash
set -e
main_dir="/var/opt/adminset"
adminset_dir="$main_dir/main"
data_dir="$main_dir/data"
config_dir="$main_dir/config"
logs_dir="$main_dir/logs"
cd "$( dirname "$0"  )"
cd .. && cd ..
cur_dir=$(pwd)

# 检测系统类型
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "无法确定操作系统类型，退出安装"
    exit 1
fi

# 同步文件
rsync --progress -ra --delete --exclude '.git' $cur_dir/ $adminset_dir

# 确定Python/pip命令
if [ "$OS" == "ubuntu" ]; then
    PIP_CMD="pip3"
    PYTHON_CMD="python3"
else
    PIP_CMD="pip"
    PYTHON_CMD="python"
fi

# 安装依赖
cd $adminset_dir
$PIP_CMD install -r requirements.txt

# SQL迁移
if [ $1 ]; then
    $PYTHON_CMD manage.py makemigrations
    for app in $*
    do
        $PYTHON_CMD manage.py migrate $app
    done
else
    $PYTHON_CMD manage.py makemigrations
    $PYTHON_CMD manage.py migrate
fi

echo "####更新celery配置####"
mkdir -p $config_dir/celery
cp $adminset_dir/install/server/celery/beat.conf $config_dir/celery/beat.conf
cp $adminset_dir/install/server/celery/celery.service /usr/lib/systemd/system
cp $adminset_dir/install/server/celery/start_celery.sh $config_dir/celery/start_celery.sh
cp $adminset_dir/install/server/celery/beat.service /usr/lib/systemd/system
chmod +x $config_dir/celery/start_celery.sh

# 根据不同系统配置nginx
if [ "$OS" == "ubuntu" ]; then
    cp $adminset_dir/install/server/nginx/adminset.conf /etc/nginx/sites-available/
    ln -sf /etc/nginx/sites-available/adminset.conf /etc/nginx/sites-enabled/
else
    cp $adminset_dir/install/server/nginx/adminset.conf /etc/nginx/conf.d
    cp $adminset_dir/install/server/nginx/nginx.conf /etc/nginx
fi

cp $adminset_dir/install/server/webssh/webssh.service /usr/lib/systemd/system
nginx -s reload

echo "##############更新完成###################"
systemctl daemon-reload
nginx -s reload
systemctl restart adminset
systemctl restart celery
echo "您已成功更新AdminSet!!!"
echo "################################################"
