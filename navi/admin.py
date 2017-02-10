from django.contrib import admin
from .models import navi

class NaviAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'url',
        ]


admin.site.register(navi, NaviAdmin)

