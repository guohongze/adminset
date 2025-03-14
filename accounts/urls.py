from django.urls import path, include
from accounts import user, role, permission, gldap


urlpatterns = [
    # path('', user.user_list, name='accounts'),
    path('login/', user.login, name='login'),
    path('logout/', user.logout, name='logout'),
    path('userlist/', user.user_list, name='user_list'),
    path('useradd/', user.user_add, name='user_add'),
    path('userdelete/<int:ids>/', user.user_del, name='user_del'),
    path('useredit/<int:ids>/', user.user_edit, name='user_edit'),
    path('resetpassword/<int:ids>/', user.reset_password, name='reset_password'),
    path('changepassword/', user.change_password, name='change_password'),
    path('changeldappassword/', user.change_ldap, name='change_ldap_password'),
    path('roleadd/', role.role_add, name='role_add'),
    path('rolelist/', role.role_list, name='role_list'),
    path('roleedit/<int:ids>/', role.role_edit, name='role_edit'),
    path('roledelete/<int:ids>/', role.role_del, name='role_del'),
    path('permdeny/', permission.permission_deny, name='permission_deny'),
    path('permadd/', permission.permission_add, name='permission_add'),
    path('permlist/', permission.permission_list, name='permission_list'),
    path('permedit/<int:ids>/', permission.permission_edit, name='permission_edit'),
    path('permdel/<int:ids>/', permission.permission_del, name='permission_del'),
    path('permission/user_permission/', permission.get_user_permission, name='get_user_permission'),
]