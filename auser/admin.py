from django.contrib import admin
from models import SysUser
# Register your models here.


class SysUserAdmin(admin.ModelAdmin):
    list_display = ['username', ]

admin.site.register(SysUser, SysUserAdmin)