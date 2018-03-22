from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
import adminset.views

urlpatterns = [
    url(r'^$', adminset.views.index, name='index'),
    url(r'^cmdb/', include('cmdb.urls')),
    url(r'^navi/', include('navi.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^setup/', include('setup.urls')),
    url(r'^monitor/', include('monitor.urls')),
    url(r'^config/', include('config.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^appconf/', include('appconf.urls')),
    url(r'^delivery/', include('delivery.urls')),
    url(r'^ossmanager/', include('oss_manager_file.urls')),
]