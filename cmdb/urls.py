from django.urls import path
from cmdb import api, idc, asset, group, cabinet


urlpatterns = [
    path('asset/', asset.asset, name='cmdb'),
    path('assetadd/', asset.asset_add, name='asset_add'),
    path('assetdel/', asset.asset_del, name='asset_del'),
    path('assetimport/', asset.asset_import, name='asset_import'),
    path('assetedit/<int:ids>/', asset.asset_edit, name='asset_edit'),
    path('asset/detail/<int:ids>/', asset.server_detail, name='server_detail'),
    # path('asset/save/', asset.asset_save, name='asset_save'),
    path('group/', group.group, name='group'),
    path('groupdel/', group.group_del, name='group_del'),
    path('groupadd/', group.group_add, name='group_add'),
    path('groupserverlist/<int:group_id>/', group.server_list, name='group_server_list'),
    path('groupedit/<int:group_id>/', group.group_edit, name='group_edit'),
    # path('group/save/', group.group_save, name='group_save'),
    path('cabinet/', cabinet.cabinet, name='cabinet'),
    path('cabinetdel/', cabinet.cabinet_del, name='cabinet_del'),
    path('cabinetadd/', cabinet.cabinet_add, name='cabinet_add'),
    path('cabinetserverlist/<int:cabinet_id>/', cabinet.server_list, name='cabinet_server_list'),
    path('cabinetedit/<int:cabinet_id>/', cabinet.cabinet_edit, name='cabinet_edit'),
    path('idc/', idc.idc, name='idc'),
    path('idcadd/', idc.idc_add, name='idc_add'),
    path('idcdel/', idc.idc_del, name='idc_del'),
    path('idcedit/<int:idc_id>/', idc.idc_edit, name='idc_edit'),
    path('idccabinetlist/<int:idc_id>/', idc.cabinet_list, name='idc_cabinet_list'),
    path('collect', api.collect, name='update_api'),
    path('gethost/', api.get_host, name='get_host'),
    path('getgroup/', api.get_group, name='get_group'),
    path('nodestatus/<int:ids>/', asset.node_status, name='node_status'),
]