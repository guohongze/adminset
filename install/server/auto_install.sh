#!/bin/bash
set -e

# 检查是否有管理员权限
if [ $(id -u) -ne 0 ]; then
    echo "请以root用户运行此脚本或使用sudo运行"
    echo "例如: sudo $0"
    exit 1
fi

# 检测操作系统类型
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [[ "$ID" != "ubuntu" || $(echo "$VERSION_ID < 24.04" | bc -l) -eq 1 ]]; then
        echo "错误: 此脚本仅支持Ubuntu 24.04系统"
        exit 1
    fi
    echo "检测到操作系统: Ubuntu $VERSION_ID"
else
    echo "错误: 无法检测操作系统类型，此脚本仅支持Ubuntu 24.04"
    exit 1
fi


# 清理旧安装
if [ -d "/var/opt/adminset" ]; then
    echo "####检测到旧安装####"
    echo "警告: 清理操作将会删除所有现有AdminSet数据和文件!"
    echo "您选择不清理旧安装，将在现有文件上进行安装"
    echo "请确认是否继续 (输入 Y 确认): "
    read -r confirm
    
    if [ "$confirm" = "Y" ]; then
        echo "开始执行清理操作..."
        
        # 检查并停止相关服务
        echo "检查并停止正在运行的相关服务..."
        
        # 定义需要检查和停止的服务列表
        services=("adminset" "webssh" "celery" "beat" "nginx" "redis-server" "mongod")
        
        # 遍历服务列表检查并停止
        for service in "${services[@]}"; do
            # 检查服务是否存在并运行
            if systemctl is-active --quiet "$service" 2>/dev/null; then
                echo "服务 $service 正在运行，尝试停止..."
                if ! systemctl stop "$service" 2>/dev/null; then
                    echo "警告: 无法停止 $service 服务，但安装将继续"
                else
                    echo "服务 $service 已成功停止"
                fi
            else
                echo "服务 $service 未运行或不存在"
            fi
        done
        
        # 尝试禁用服务（可选）
        echo "尝试禁用服务..."
        for service in "${services[@]}"; do
            if systemctl is-enabled --quiet "$service" 2>/dev/null; then
                systemctl disable "$service" 2>/dev/null || echo "警告: 无法禁用 $service 服务"
            fi
        done
        
        # 检查是否有相关进程仍在运行（使用进程名查找）
        echo "检查是否有相关进程仍在运行..."
        process_names=("gunicorn" "wssh" "celery" "nginx" "redis-server" "mongod")
        for proc in "${process_names[@]}"; do
            if pgrep -f "$proc" > /dev/null; then
                echo "发现 $proc 进程仍在运行，尝试终止..."
                pkill -f "$proc" || echo "警告: 无法终止 $proc 进程，但安装将继续"
            fi
        done
        
        # 检查是否有使用特定端口的进程
        ports=(8000 8888 80 443 27017 6379)
        for port in "${ports[@]}"; do
            if lsof -i:"$port" > /dev/null 2>&1; then
                echo "发现端口 $port 被占用，尝试释放..."
                fuser -k "$port"/tcp > /dev/null 2>&1 || echo "警告: 无法释放端口 $port，但安装将继续"
            fi
        done
        
        # 停止现有服务（原有代码，保留以防部分服务未被上面的步骤停止）
        echo "停止现有服务..."
        systemctl stop adminset webssh celery beat 2>/dev/null || true
        
        # 删除数据库
        echo "删除旧数据库..."
        if command -v mysql &> /dev/null; then
            mysql -e "DROP DATABASE IF EXISTS adminset;" 2>/dev/null || true
        fi
        
        # 清理文件
        echo "删除旧安装文件..."
        rm -rf /var/opt/adminset/main/*
        
        echo "旧安装清理完成"
    else
        echo "您选择不清理旧安装，将在现有文件上进行安装"
        echo "注意: 这可能会导致冲突或安装问题"
    fi
fi
# 配置CSRF信任域名（提前收集用户输入）
echo "####配置CSRF信任域名####"
echo "为了确保Django CSRF保护正常工作，需要配置可信任的域名"
echo "请输入您将用于访问AdminSet的完整域名或IP地址（包括协议，如 https://www.example.com 或 http://192.168.110.100）:"
read -r domain_input

# 去除输入的空格
domain_input=$(echo "$domain_input" | xargs)

# 设置默认域名
default_domains=("https://192.168.110.100" "http://192.168.110.100")

# 验证域名格式
domain_valid=0
# 检查是否是有效的URL格式 (支持域名或IP地址)
if [[ "$domain_input" =~ ^https?:// ]]; then
    # 验证URL的基本结构
    protocol=$(echo "$domain_input" | cut -d'/' -f1)
    host=$(echo "$domain_input" | cut -d'/' -f3)
    
    if [[ -n "$host" ]]; then
        # 验证是IP地址还是域名
        if [[ "$host" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            # 简单IP地址格式验证
            domain_valid=1
            echo "IP地址格式有效: $domain_input"
        elif [[ "$host" =~ ^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$ ]]; then
            # 域名格式验证
            domain_valid=1
            echo "域名格式有效: $domain_input"
        fi
    fi
fi

if [ $domain_valid -eq 0 ]; then
    echo "警告: 输入的域名/IP地址格式无效: $domain_input"
    echo "正确的格式应该是: https://www.example.com 或 http://192.168.1.100"
    echo "Django 4.0+要求所有CSRF_TRUSTED_ORIGINS值必须以http://或https://开头"
    echo "由于输入格式无效，将使用默认值: ${default_domains[0]} 和 ${default_domains[1]}"
    # 不再尝试修复无效输入，直接使用默认值
    domain_input=""
    domain_valid=0
fi

# 初始化环境目录
main_dir="/var/opt/adminset"
adminset_dir="$main_dir/main"
data_dir="$main_dir/data"
config_dir="$main_dir/config"
logs_dir="$main_dir/logs"
venv_dir="$main_dir/venv"  # Python虚拟环境目录

cd "$( dirname "$0"  )"
cd .. && cd ..
cur_dir=$(pwd)
mkdir -p $adminset_dir
mkdir -p $data_dir/scripts
mkdir -p $data_dir/files
mkdir -p $data_dir/ansible/playbook
mkdir -p $data_dir/ansible/roles
mkdir -p $config_dir
mkdir -p $config_dir/webssh
mkdir -p $logs_dir
mkdir -p $logs_dir/execlog
mkdir -p $main_dir/pid

# 安装依赖包
echo "####安装依赖包####"
apt-get update
apt-get install -y python3 python3-pip python3-dev python3-venv python3-full build-essential libssl-dev 
# 添加pkg-config和MariaDB开发库以解决mysqlclient编译问题（避免与MySQL开发库冲突）
apt-get install -y libmariadb-dev libmariadb-dev-compat pkg-config libsasl2-dev libldap2-dev git rsync expect
apt-get install -y smartmontools dmidecode ansible bc

# 分发代码
if [ ! $cur_dir ] || [ ! $adminset_dir ]; then
    echo "安装目录信息错误，请检查您的系统环境"
    exit 1
else
    rsync --delete --progress -ra --exclude '.git' $cur_dir/ $adminset_dir
fi

# 配置ansible
if [ ! -d /etc/ansible ]; then
    mkdir -p /etc/ansible
fi
cp $adminset_dir/install/server/ansible/ansible.cfg /etc/ansible/ansible.cfg

# 安装数据库
echo "####安装数据库####"
echo "正在安装MariaDB..."
apt-get install -y mariadb-server libmariadb-dev
systemctl start mariadb
mysql -e "DROP DATABASE IF EXISTS adminset;"
mysql -e "CREATE DATABASE adminset CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
systemctl enable mariadb.service

# 修复现有的CSRF_TRUSTED_ORIGINS值
settings_file="$adminset_dir/adminset/settings.py"
if [ -f "$settings_file" ]; then
    # 首先检查是否存在不符合要求的配置项（没有http://或https://前缀的项）
    if grep -q "CSRF_TRUSTED_ORIGINS.*['\"][^h][^t][^t][^p]" "$settings_file" || grep -q "CSRF_TRUSTED_ORIGINS.*['\"]\.[^/]" "$settings_file"; then
        echo "检测到现有CSRF_TRUSTED_ORIGINS中存在不符合Django 4.0+要求的项（缺少http://或https://前缀）"
        echo "正在修复现有配置..."
        
        # 创建临时文件
        temp_file=$(mktemp)
        
        # 使用awk处理每一行，修复不符合要求的项
        awk '
        /CSRF_TRUSTED_ORIGINS.*=.*\[/ {
            print $0
            in_csrf_list = 1
            next
        }
        in_csrf_list && /\]/ {
            in_csrf_list = 0
            print $0
            next
        }
        in_csrf_list && /[^\047"]*[^\047"]([\047"])([^h][^t][^t][^p]|\.)[^\047"]*[\047"]/ {
            # 替换不带协议前缀的域名/IP
            gsub(/([\047"])([^h][^t][^t][^p]|\.)[^\047"]*[\047"]/, "\\1http://\\2\\1")
            print $0
            next
        }
        {
            print $0
        }
        ' "$settings_file" > "$temp_file"
        
        # 将临时文件内容复制回原文件
        cat "$temp_file" > "$settings_file"
        rm "$temp_file"
        
        echo "完成修复CSRF_TRUSTED_ORIGINS中的现有项"
    fi
    
    if [ $domain_valid -eq 1 ]; then
        # 如果用户输入了有效域名，检查是否已存在
        if grep -q "CSRF_TRUSTED_ORIGINS.*['\"]$domain_input['\"]" "$settings_file"; then
            echo "域名 $domain_input 已存在于CSRF信任列表中，跳过添加。"
        else
            # 检查CSRF_TRUSTED_ORIGINS是否存在
            if grep -q "CSRF_TRUSTED_ORIGINS" "$settings_file"; then
                # 在CSRF_TRUSTED_ORIGINS列表中添加新域名
                sed -i "/CSRF_TRUSTED_ORIGINS.*\[/ a\\    '$domain_input'," "$settings_file"
                echo "已将 $domain_input 添加到CSRF信任列表。"
            else
                # 如果CSRF_TRUSTED_ORIGINS不存在，创建新的配置块
                # 找到"# CSRF设置"行，如果不存在则找到一个合适的位置
                if grep -q "# CSRF设置" "$settings_file"; then
                    sed -i "/# CSRF设置/ a\\CSRF_TRUSTED_ORIGINS = [\n    '$domain_input',\n]" "$settings_file"
                else
                    # 在ALLOWED_HOSTS后面添加
                    sed -i "/ALLOWED_HOSTS.*/ a\\\\n# CSRF设置\\nCSRF_TRUSTED_ORIGINS = [\n    '$domain_input',\n]" "$settings_file"
                fi
                echo "已创建CSRF信任列表并添加 $domain_input。"
            fi
        fi
    else
        # 无效输入情况下，检查是否需要添加默认域名
        csrf_exists=0
        if grep -q "CSRF_TRUSTED_ORIGINS" "$settings_file"; then
            csrf_exists=1
        fi
        
        if [ $csrf_exists -eq 0 ]; then
            # 如果不存在CSRF_TRUSTED_ORIGINS，使用默认值创建
            echo "使用默认CSRF信任域名创建配置..."
            if grep -q "# CSRF设置" "$settings_file"; then
                sed -i "/# CSRF设置/ a\\CSRF_TRUSTED_ORIGINS = [\n    '${default_domains[0]}',\n    '${default_domains[1]}',\n]" "$settings_file"
            else
                sed -i "/ALLOWED_HOSTS.*/ a\\\\n# CSRF设置\\nCSRF_TRUSTED_ORIGINS = [\n    '${default_domains[0]}',\n    '${default_domains[1]}',\n]" "$settings_file"
            fi
            echo "已使用默认域名创建CSRF信任列表。"
        else
            echo "保留现有CSRF信任域名配置。"
        fi
    fi
else
    echo "警告: 找不到settings.py文件，无法配置CSRF信任域名。"
    echo "请在安装完成后手动配置: $settings_file"
fi

# 安装mongodb
echo "####安装MongoDB####"
echo "正在安装MongoDB 8.0..."

# 安装必要的依赖包
apt-get install -y gnupg curl

# 移除任何已存在的MongoDB仓库配置
rm -f /etc/apt/sources.list.d/mongodb-org-*.list

# 导入MongoDB 8.0 GPG密钥
curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
    gpg --yes --dearmor -o /usr/share/keyrings/mongodb-server-8.0.gpg

# 使用jammy仓库安装MongoDB 8.0（确保兼容性）
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 multiverse" | \
    tee /etc/apt/sources.list.d/mongodb-org-8.0.list

# 更新包索引
apt-get update -y

# 安装MongoDB 8.0
apt-get install -y mongodb-org

# 启动MongoDB服务
systemctl daemon-reload
systemctl start mongod
systemctl enable mongod

# 确认安装成功
echo "MongoDB 8.0安装完成！"

# 创建Python虚拟环境
echo "####创建Python虚拟环境####"
python3 -m venv $venv_dir
source $venv_dir/bin/activate

# 配置pip源
mkdir -p ~/.pip
cat <<EOF > ~/.pip/pip.conf
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
EOF

# 安装主程序
echo "####安装AdminSet####"
# 升级pip和安装setuptools
$venv_dir/bin/pip install --upgrade pip
$venv_dir/bin/pip install --upgrade setuptools wheel

# 安装特定版本的celery以避免无效依赖问题
$venv_dir/bin/pip install celery==5.3.6
$venv_dir/bin/pip install django-celery-results==2.5.1


# 安装项目依赖
cd $adminset_dir
$venv_dir/bin/pip install -r requirements.txt

# 执行数据库迁移
echo "执行数据库迁移..."
# 清理所有现有迁移文件，使用全自动生成
echo "清理所有现有迁移文件..."
find $adminset_dir -path "*/migrations/[0-9]*.py" -delete

# 创建必要的迁移目录和初始化文件
for app in accounts appconf cmdb config setup; do
    mkdir -p $adminset_dir/$app/migrations
    touch $adminset_dir/$app/migrations/__init__.py
done

# 修复潜在的外键约束问题
echo "配置MySQL以处理外键约束..."
mysql -e "SET GLOBAL foreign_key_checks=0;" 2>/dev/null || true

# 按正确顺序生成迁移文件
echo "生成迁移文件..."
# 首先为核心和基础应用创建迁移文件
$venv_dir/bin/python manage.py makemigrations appconf
$venv_dir/bin/python manage.py makemigrations cmdb
$venv_dir/bin/python manage.py makemigrations config setup
# 最后为accounts创建迁移文件，因为它依赖其他应用
$venv_dir/bin/python manage.py makemigrations accounts

# 使用更通用的迁移方法，避免指定可能不存在的应用
echo "应用迁移..."
# 首先迁移所有可能的默认应用
$venv_dir/bin/python manage.py migrate

# 然后尝试单独迁移每个已知应用
echo "迁移核心应用..."
for app in appconf cmdb config setup accounts; do
    echo "迁移 $app 应用..."
    if ! $venv_dir/bin/python manage.py migrate $app 2>/dev/null; then
        echo "$app 迁移失败，尝试使用--fake-initial..."
        if ! $venv_dir/bin/python manage.py migrate $app --fake-initial 2>/dev/null; then
            echo "警告: $app 迁移仍然失败，将继续安装过程"
        fi
    fi
done

# 最后确保所有表都已创建
$venv_dir/bin/python manage.py migrate --run-syncdb

# 恢复MySQL外键检查
mysql -e "SET GLOBAL foreign_key_checks=1;" 2>/dev/null || true

echo "注意: 默认管理员账号admin，密码admin"
source /etc/profile

# 创建默认管理员 - 双重保障方案
# 创建脚本文件
cat > $adminset_dir/create_admin.py << EOF
#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adminset.settings")
django.setup()

from accounts.models import UserInfo
import MySQLdb

# 1. 尝试通过Django ORM创建用户
try:
    if not UserInfo.objects.filter(username='admin').exists():
        admin = UserInfo.objects.create_superuser(
            email='admin@126.com',
            username='admin',
            password='admin'
        )
        print("管理员用户已通过ORM创建，用户名: admin, 密码: admin")
    else:
        print("管理员用户已存在")
except Exception as e:
    print(f"通过ORM创建管理员失败: {e}")
    
    # 2. 如果ORM方式失败，尝试直接SQL方式创建
    try:
        db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="adminset")
        cursor = db.cursor()
        
        # 检查表是否存在
        cursor.execute("SHOW TABLES LIKE 'accounts_userinfo'")
        if cursor.fetchone():
            # 检查用户是否存在
            cursor.execute("SELECT id FROM accounts_userinfo WHERE username='admin'")
            if not cursor.fetchone():
                # 加密密码哈希 - 这是Django的pbkdf2_sha256算法生成的值，对应明文'admin'
                # 如果后续Django版本改变了密码哈希算法，此方式仍能工作，用户可以正常登录后修改密码
                cursor.execute("INSERT INTO accounts_userinfo (username, email, password, is_active, is_superuser) VALUES ('admin', 'admin@126.com', 'pbkdf2_sha256\$600000\$S0dKZmP9REQ8FMVtWT54kA\$hdGCdT2qP0GzZJyiH3T2nOv9ULPDQtY1h+N/NI/jILU=', 1, 1)")
                db.commit()
                print("管理员用户已通过SQL创建，用户名: admin, 密码: admin")
            else:
                print("管理员用户已存在")
        else:
            print("accounts_userinfo表不存在，无法创建管理员")
        db.close()
    except Exception as e:
        print(f"通过SQL创建管理员失败: {e}")
EOF

# 执行创建管理员脚本
chmod +x $adminset_dir/create_admin.py
if ! $venv_dir/bin/python $adminset_dir/create_admin.py; then
    echo "警告: 创建管理员账户时出现问题，但将继续安装过程"
    echo "请在安装完成后，使用以下SQL命令手动创建管理员："
    echo "mysql -e \"INSERT INTO adminset.accounts_userinfo (username, email, password, is_active, is_superuser) VALUES ('admin', 'admin@126.com', 'pbkdf2_sha256\$600000\$S0dKZmP9REQ8FMVtWT54kA\$hdGCdT2qP0GzZJyiH3T2nOv9ULPDQtY1h+N/NI/jILU=', 1, 1);\""
fi

# 修改systemd服务文件以使用虚拟环境
echo "####更新systemd服务配置####"

# 备份并修改adminset.service文件
cp $adminset_dir/install/server/adminset.service $adminset_dir/install/server/adminset.service.bak
cat > $adminset_dir/install/server/adminset.service << EOF
[Unit]
Description=AdminSet
After=network.target

[Service]
Type=simple
WorkingDirectory=/var/opt/adminset/main
ExecStart=/var/opt/adminset/venv/bin/gunicorn adminset.wsgi:application -b 0.0.0.0:8000 -w 2 -k gthread -t 2 -n 1 --access-logfile /var/opt/adminset/logs/access.log --error-logfile /var/opt/adminset/logs/error.log
ExecReload=/bin/kill -s HUP \$MAINPID
ExecStop=/bin/kill -s TERM \$MAINPID
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

# 配置WebSSH服务
echo "####配置WebSSH服务####"
cp $adminset_dir/install/server/webssh/webssh.service /usr/lib/systemd/system
systemctl daemon-reload
systemctl enable webssh
echo "WebSSH服务配置完成"

# 备份并修改celery.service文件
cp $adminset_dir/install/server/celery/celery.service $adminset_dir/install/server/celery/celery.service.bak
cat > $adminset_dir/install/server/celery/celery.service << EOF
[Unit]
Description=AdminSet Celery Worker Service
After=network.target

[Service]
Type=forking
WorkingDirectory=/var/opt/adminset/main
ExecStart=/var/opt/adminset/config/celery/start_celery.sh
ExecReload=/bin/kill -s HUP \$MAINPID
ExecStop=/bin/kill -s TERM \$MAINPID
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

# 备份并修改beat.service文件
cp $adminset_dir/install/server/celery/beat.service $adminset_dir/install/server/celery/beat.service.bak
cat > $adminset_dir/install/server/celery/beat.service << EOF
[Unit]
Description=AdminSet Beat Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/var/opt/adminset/main
ExecStart=/var/opt/adminset/venv/bin/celery -A adminset beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
ExecReload=/bin/kill -s HUP \$MAINPID
ExecStop=/bin/kill -s TERM \$MAINPID
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

# 修改start_celery.sh脚本以使用虚拟环境
cp $adminset_dir/install/server/celery/start_celery.sh $adminset_dir/install/server/celery/start_celery.sh.bak
cat > $adminset_dir/install/server/celery/start_celery.sh << EOF
#!/bin/bash
# Name: start_celery.sh
# Author: guohongze
# Created Time: 2021-10-01 10:19:01

NAME="adminset"
VENV="/var/opt/adminset/venv/bin/celery"
DJANGODIR="/var/opt/adminset/main"
USER=root
GROUP=root
NUM=4
TIMEOUT=9999
LOG_LEVEL=info
LOG_FILE="/var/opt/adminset/logs/celery-worker.log"
PID_FILE="/var/opt/adminset/pid/celery-worker.pid"
ENV_PYTHON="/var/opt/adminset/venv/bin/python"

cd \$DJANGODIR
source /var/opt/adminset/venv/bin/activate
exec \${VENV} multi start \${NAME} -A adminset --concurrency=\${NUM} --pidfile=\${PID_FILE} -l \${LOG_LEVEL} --logfile=\${LOG_FILE} -c 4 -Ofair --time-limit=\${TIMEOUT} --detach
deactivate
EOF

# 创建所需目录并设置权限
echo "创建所需的配置目录..."
mkdir -p $config_dir/celery
chmod 755 $config_dir/celery

# 设置启动脚本权限
chmod +x $adminset_dir/install/server/celery/start_celery.sh
cp $adminset_dir/install/server/celery/start_celery.sh $config_dir/celery/start_celery.sh
chmod +x $config_dir/celery/start_celery.sh

# 复制celery配置文件
cp $adminset_dir/install/server/celery/beat.conf $config_dir/celery/beat.conf
cp $adminset_dir/install/server/celery/celery.service /usr/lib/systemd/system
cp $adminset_dir/install/server/celery/beat.service /usr/lib/systemd/system

# 安装redis
echo "####安装Redis####"
apt-get install -y redis-server
systemctl start redis-server
systemctl enable redis-server

# 安装nginx
echo "####安装Nginx####"
apt-get install -y nginx

# 确保静态文件目录存在但不执行collectstatic
echo "####配置静态文件目录####"
chmod 755 /var/opt/adminset/main/static/


# 设置适当的文件权限
echo "设置静态文件权限..."
# 使用www-data用户，与Nginx默认用户保持一致
chown -R www-data:www-data /var/opt/adminset/main/static/

# 备份原始配置
echo "备份Nginx原始配置..."
[ -f /etc/nginx/nginx.conf ] && cp -f /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
[ -f /etc/nginx/sites-enabled/default ] && rm -f /etc/nginx/sites-enabled/default

# 直接复制项目中的nginx.conf文件覆盖系统文件
echo "复制Nginx主配置文件..."
cp -f $adminset_dir/install/server/nginx/nginx.conf /etc/nginx/nginx.conf

# 移除sites-available/enabled中的文件以避免冲突
rm -f /etc/nginx/sites-enabled/adminset.conf
rm -f /etc/nginx/sites-available/adminset.conf

# 确保conf.d目录存在
mkdir -p /etc/nginx/conf.d

# 使用adminset.conf.https作为主配置并复制到conf.d目录
echo "配置Nginx HTTPS支持..."
cp -f $adminset_dir/install/server/nginx/adminset.conf.https /etc/nginx/conf.d/adminset.conf

# 创建SSL证书目录并复制证书文件
echo "设置SSL证书..."
mkdir -p /etc/nginx/ssl
cp -f $adminset_dir/install/server/nginx/nginx.crt /etc/nginx/ssl/
cp -f $adminset_dir/install/server/nginx/nginx.key /etc/nginx/ssl/
chmod 600 /etc/nginx/ssl/nginx.key
chmod 644 /etc/nginx/ssl/nginx.crt

# 修复Nginx配置中的用户设置
echo "修复Nginx配置中的用户设置..."
if grep -q "user nginx;" /etc/nginx/nginx.conf; then
    echo "检测到nginx.conf中配置的是nginx用户，修改为www-data用户..."
    sed -i 's/user nginx;/user www-data;/g' /etc/nginx/nginx.conf
fi

# 验证配置
echo "验证Nginx配置..."
if ! nginx -t; then
    echo "错误: Nginx配置有误，可能是SSL证书问题，尝试使用HTTP配置..."
    # 如果HTTPS配置有问题，使用HTTP配置作为备选
    cp $adminset_dir/install/server/nginx/adminset.conf /etc/nginx/conf.d/adminset.conf
    
    # 再次验证配置
    if ! nginx -t; then
        echo "错误: HTTP配置也有问题，使用最简配置..."
        # 创建一个最简单的配置
        cat > /etc/nginx/conf.d/adminset.conf << EOF
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF
    fi
fi

# 启动nginx
echo "启动Nginx服务..."
systemctl restart nginx || true
systemctl enable nginx || true

# 如果启动失败，提供诊断信息
if ! systemctl is-active nginx >/dev/null 2>&1; then
    echo "警告: Nginx服务未能启动，但安装过程将继续"
    echo "您可以稍后使用以下命令查看错误详情："
    echo "  systemctl status nginx"
    echo "  journalctl -xeu nginx.service"
    echo "您也可以直接访问AdminSet提供的端口: http://服务器IP:8000"
fi

# 清理不再需要的依赖包
echo "####清理不再需要的依赖包####"
apt autoremove -y

# 创建SSH配置
echo "创建SSH密钥..."
if [ ! -e ~/.ssh/id_rsa.pub ]; then
    ssh-keygen -q -N "" -t rsa -f /root/.ssh/id_rsa
fi
cp $adminset_dir/install/server/ssh/config ~/.ssh/config

# 完成安装
echo "#######等待启动服务##############"

# 检查并修复adminset.service中的参数问题
echo "检查AdminSet服务配置..."
if [ -f "/usr/lib/systemd/system/adminset.service" ]; then
    # 确保日志目录存在
    mkdir -p /var/opt/adminset/logs
    mkdir -p /var/opt/adminset/pid
    
    # 检查adminset.service文件是否可能有问题
    if grep -q -- "-d" /usr/lib/systemd/system/adminset.service || ! grep -q "WorkingDirectory" /usr/lib/systemd/system/adminset.service || ! systemctl is-active adminset > /dev/null 2>&1; then
        echo "检测到AdminSet服务配置可能有问题，尝试修复..."
        
        # 备份原始配置
        cp /usr/lib/systemd/system/adminset.service /tmp/adminset.service.bak
        
        # 设置正确的服务配置
        cat > /usr/lib/systemd/system/adminset.service << EOF
[Unit]
Description=AdminSet
After=network.target

[Service]
Type=simple
WorkingDirectory=/var/opt/adminset/main
ExecStart=/var/opt/adminset/venv/bin/gunicorn adminset.wsgi:application -b 0.0.0.0:8000 -w 2 -k gthread -t 2 -n 1 --access-logfile /var/opt/adminset/logs/access.log --error-logfile /var/opt/adminset/logs/error.log
ExecReload=/bin/kill -s HUP \$MAINPID
ExecStop=/bin/kill -s TERM \$MAINPID
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF
        
        echo "AdminSet服务配置已修复"
    else
        echo "AdminSet服务配置无需修复"
    fi
fi

systemctl daemon-reload
systemctl restart mariadb
systemctl restart mongod
systemctl restart celery
systemctl restart beat

# 启动AdminSet服务
echo "启动AdminSet服务..."
systemctl restart adminset

# 等待几秒钟服务启动
sleep 3

# 检查AdminSet服务状态
adminset_status=$(systemctl is-active adminset)
if [ "$adminset_status" != "active" ]; then
    echo "AdminSet服务启动失败，尝试进一步检查和修复..."
    
    # 检查必要目录和文件
    if [ ! -d "/var/opt/adminset/main" ]; then
        echo "错误: 缺少主应用目录，请确保安装过程正确完成"
    else
        echo "尝试修复AdminSet服务配置..."
        
        # 确保PID和日志目录存在并有正确权限
        mkdir -p /var/opt/adminset/pid
        mkdir -p /var/opt/adminset/logs
        chmod 755 /var/opt/adminset/pid
        chmod 755 /var/opt/adminset/logs
        
        # 使用最简化的服务配置
        cat > /usr/lib/systemd/system/adminset.service << EOF
[Unit]
Description=AdminSet
After=network.target

[Service]
Type=simple
WorkingDirectory=/var/opt/adminset/main
ExecStart=/var/opt/adminset/venv/bin/gunicorn adminset.wsgi:application -b 0.0.0.0:8000 -w 2 -k gthread -t 2 -n 1 --access-logfile /var/opt/adminset/logs/access.log --error-logfile /var/opt/adminset/logs/error.log
ExecReload=/bin/kill -s HUP \$MAINPID
ExecStop=/bin/kill -s TERM \$MAINPID
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF
        
        # 重新加载和启动
        systemctl daemon-reload
        systemctl restart adminset
        
        # 再次检查
        sleep 3
        if [ "$(systemctl is-active adminset)" != "active" ]; then
            echo "警告: AdminSet服务仍然无法启动，请查看日志获取详细信息:"
            echo "  journalctl -xeu adminset.service"
            echo "您仍然可以使用Django开发服务器启动应用程序："
            echo "  cd /var/opt/adminset/main && /var/opt/adminset/venv/bin/python manage.py runserver 0.0.0.0:8000"
        else
            echo "AdminSet服务已成功修复并启动"
        fi
    fi
else
    echo "AdminSet服务已成功启动"
fi
# 备份原文件并强制复制新的 index.html
cp -f /var/opt/adminset/venv/lib/python3.12/site-packages/webssh/templates/index.html /var/opt/adminset/venv/lib/python3.12/site-packages/webssh/templates/index.html.bak 2>/dev/null || true
cp -f $adminset_dir/templates/vendor/webssh/index.html /var/opt/adminset/venv/lib/python3.12/site-packages/webssh/templates/index.html
systemctl restart webssh
systemctl restart nginx
systemctl restart sshd
echo "请访问网站 http://服务器IP"
echo "默认管理员账号为admin,密码为admin,请尽快更改"
echo "恭喜，您已成功安装AdminSet!"
echo "################################################"