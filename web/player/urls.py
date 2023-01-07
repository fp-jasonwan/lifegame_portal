from django.contrib import admin
from django.urls import path, include
from player import views

urlpatterns = [
    path('<str:user_id>', views.get_profile, name='profile_by_userid'),
    path('', views.get_profile, name='self_profile'),
    path('qrcode', views.get_profile_qrcode, name='qrcode'),
]