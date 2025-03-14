#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adminset.settings")
django.setup()

from accounts.models import UserInfo

# 检查用户是否存在
if not UserInfo.objects.filter(username='admin').exists():
    # 创建管理员用户
    admin = UserInfo.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        password='admin'
    )
    print("管理员用户已创建，用户名: admin, 密码: admin")
else:
    print("管理员用户已存在") 