from django.urls import path, include  # 更新为Django新版的path和include
# from django.contrib import admin  # 移除admin导入
from django.conf import settings
from adminset.views import index
from cmdb import asset
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('', index, name='index'),
    path('cmdb/', include('cmdb.urls')),
    path('navi/', include('navi.urls')),
    # path('admin/', admin.site.urls),  # 移除admin URL路径
    path('setup/', include('setup.urls')),
    path('monitor/', include('monitor.urls')),
    path('config/', include('config.urls')),
    path('accounts/', include('accounts.urls')),
    path('appconf/', include('appconf.urls')),
    path('delivery/', include('delivery.urls')),
    path('mfile/', include('mfile.urls')),
    path('elfinder/', include('elfinder.urls')),
    path('branches/', include('branches.urls')),
    path('webssh/<int:ids>/', asset.webssh, name='webssh'),  # 已删除webssh功能
    
    # 添加媒体文件URL，确保能够访问上传的文件
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]