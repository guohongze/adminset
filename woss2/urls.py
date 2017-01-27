from django.conf.urls import include,url
from django.contrib import admin

urlpatterns = [
    url(r'^cmdb/', include('cmdb.urls')),
    url(r'^api/', include('app01.urls')),
    url(r'^token/', include('app02.urls')),
    url(r'^admin/', admin.site.urls),
]