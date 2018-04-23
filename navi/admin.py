from django.contrib import admin
from .models import navi


class NaviAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'url',
        ]


admin.site.register(navi, NaviAdmin)

