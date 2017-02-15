#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Host, HostGroup, IpSource, Idc, InterFace, UserInfo


class HostAdmin(admin.ModelAdmin):
    list_display = [
        'hostname',
        'ip',
        'group',
        'vendor',
        'os',
        'cpu_model',
        'cpu_num',
        'sn',
        #'identity',
        ]


class HostGroupAdmin(admin.ModelAdmin):
    list_display = ['name',]


class IpAdmin(admin.ModelAdmin):
    list_display = ['net',]


class IdcAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'address',
                    ]


class InterFaceAdmin(admin.ModelAdmin):
    list_display = ['name',]

admin.site.register(Host, HostAdmin)
admin.site.register(IpSource, IpAdmin)
admin.site.register(Idc, IdcAdmin)
admin.site.register(InterFace, InterFaceAdmin)
admin.site.register(HostGroup, HostGroupAdmin)
admin.site.register(UserInfo)