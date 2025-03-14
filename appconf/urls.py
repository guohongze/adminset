from django.urls import path, include
from appconf import product, project, appowner, authinfo

urlpatterns = [
    path('appowneradd/', appowner.appowner_add, name='appowner_add'),
    path('appowneraddmini/', appowner.appowner_add_mini, name='appowner_add_mini'),
    path('appowner/', appowner.appowner_list, name='appowner_list'),
    path('appowneredit/<int:appowner_id>/', appowner.appowner_edit, name='appowner_edit'),
    path('appownerdel/', appowner.appowner_del, name='appowner_del'),
    path('productadd/', product.product_add, name='product_add'),
    path('product/', product.product_list, name='product_list'),
    path('productplist/<int:product_id>/', product.project_list, name='product_project_list'),
    path('productedit/<int:product_id>/', product.product_edit, name='product_edit'),
    path('productdel/', product.product_del, name='product_del'),
    path('projectadd/', project.project_add, name='project_add'),
    path('project/', project.project_list, name='project_list'),
    path('projectedit/<int:project_id>/', project.project_edit, name='project_edit'),
    path('projectdel/', project.project_del, name='project_del'),
    path('projectexport/', project.project_export, name='project_export'),
    path('authinfoadd/', authinfo.authinfo_add, name='authinfo_add'),
    path('authinfoaddmini/', authinfo.authinfo_add_mini, name='authinfo_add_mini'),
    path('authinfo/', authinfo.authinfo_list, name='authinfo_list'),
    path('authinfoedit/<int:authinfo_id>/', authinfo.authinfo_edit, name='authinfo_edit'),
    path('authinfodel/', authinfo.authinfo_del, name='authinfo_del'),
]
