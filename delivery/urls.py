from django.urls import path
from delivery import deli, tasks

urlpatterns = [
    path('deliadd/', deli.delivery_add, name='delivery_add'),
    path('delilist/', deli.delivery_list, name='delivery_list'),
    path('delistatus/<int:project_id>/', deli.status, name='delivery_status'),
    path('deliedit/<int:project_id>/', deli.delivery_edit, name='delivery_edit'),
    path('delilog/<int:project_id>/', deli.log, name='delivery_log'),
    path('delilog2/<int:project_id>/', deli.log2, name='delivery_log2'),
    path('delilogdel/', deli.log_del, name='log_del'),
    path('delilogdelall/', deli.log_delall, name='log_delall'),
    path('delilogshistory/<int:project_id>/', deli.logs_history, name='logs_history'),
    path('deligetlogs/<int:project_id>/<str:logname>/', deli.get_log, name='get_log'),
    path('delideploy/<int:project_id>/', deli.delivery_deploy, name='delivery_deploy'),
    path('delitaskstop/<int:project_id>/', deli.task_stop, name='delivery_taskstop'),
    path('delidel/', deli.delivery_del, name='delivery_del'),
]
