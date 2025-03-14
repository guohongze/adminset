from django.urls import path, include
from branches import region, branch, resource

urlpatterns = [
    path('', region.region_list, name='branches'),
    path('regionadd/', region.region_add, name='region_add'),
    path('region/', region.region_list, name='region_list'),
    path('regionbranchinfo/<int:region_id>/', region.branch_detail, name='branch_detail'),
    path('regionedit/<int:region_id>/', region.region_edit, name='region_edit'),
    path('regiondel/', region.region_del, name='region_del'),
    path('branchadd/', branch.branch_add, name='branch_add'),
    path('branch/', branch.branch_list, name='branch_list'),
    path('branchedit/<int:branch_id>/', branch.branch_edit, name='branch_edit'),
    path('branchdel/', branch.branch_del, name='branch_del'),
    path('branchexport/', branch.branch_export, name='branch_export'),
    path('branchresourceinfo/<int:branch_id>/', branch.resource_detail, name='resource_detail'),
    path('resourceadd/', resource.resource_add, name='resource_add'),
    path('resource/', resource.resource_list, name='resource_list'),
    path('resourceedit/<int:resource_id>/', resource.resource_edit, name='resource_edit'),
    path('resourcedel/', resource.resource_del, name='resource_del'),
    path('resourceexport/', resource.resource_export, name='resource_export'),
]