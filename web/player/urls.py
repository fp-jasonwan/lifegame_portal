from django.contrib import admin
from django.urls import path, include
from player import views

urlpatterns = [
    path('', views.get_profile, name='self_profile'),
]