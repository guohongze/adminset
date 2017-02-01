from django.conf.urls import include,url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^cmdb/', include('cmdb.urls')),
    url(r'^admin/', admin.site.urls),
]
#urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)