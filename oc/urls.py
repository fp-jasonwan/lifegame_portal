from .views import oc_portal, search_profile, list_booth, booth_home, check_player, register_player, register_page
from django.urls import path, include

urlpatterns = [
    path('', oc_portal, name='oc_portal'),
    path('search_profile', search_profile, name='search_profile'),
    path('booth_list', list_booth, name='list_booth'),
    path('booth/<str:booth_id>/', booth_home, name='booth_home'),
    path('booth/<str:booth_id>/check_player/<int:user_id>', check_player, name='check_player'),
    path('booth/<str:booth_id>/check_player', check_player, name='check_player'),

    path('booth/<str:booth_id>/register/<int:user_id>', register_player, name='register_player')
]