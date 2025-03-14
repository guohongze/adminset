from django.urls import path, re_path
from monitor import system, manage, api

urlpatterns = [
    path('system/', system.index, name='monitor'),
    path('manage/delall/', manage.drop_sys_info, name='drop_all'),
    path('hosttree/', system.tree_node, name='host_tree'),
    re_path(r'^manage/delrange/(?P<timing>[0-9])/$', manage.del_monitor_data, name='del_monitor_data'),
    path('manage/', manage.index, name='monitor_manage'),
    re_path(r'^system/(?P<hostname>.+)/(?P<timing>\d+)/$', system.host_info, name='host_info'),
    re_path(r'^getcpu/(?P<hostname>.+)/(?P<timing>\d+)/$', system.get_cpu, name='get_cpu'),
    re_path(r'^getmem/(?P<hostname>.+)/(?P<timing>\d+)/$', system.get_mem, name='get_mem'),
    re_path(r'^getdisk/(?P<hostname>.+)/(?P<timing>\d+)/(?P<partition>\d+)/$', system.get_disk, name='get_disk'),
    re_path(r'^getnet/(?P<hostname>.+)/(?P<timing>\d+)/(?P<net_id>\d+)/$', system.get_net, name='get_net'),
    path('received/sys/info/', api.received_sys_info, name='received_sys_info'),
]