from django.urls import path, include
from config import views


urlpatterns = [
    path('', views.index, name='config'),
    path('config_save/', views.config_save, name='config_save'),
    path('token/', views.get_token, name='token'),
]