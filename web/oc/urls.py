from .views import oc_portal, search_profile, list_booth, booth_home, check_player, register_player, register_page, get_instructor_players, register_instructor_comment
from .views import register
from django.urls import path, include
from booth.views import get_parti_record, get_traffic_record
urlpatterns = [
    path('', oc_portal, name='oc_portal'),
    path('register', register, name="register"),
    path('search_profile', search_profile, name='search_profile'),
    path('search_profile/<int:user_id>', search_profile, name='search_profile_with_id'),
    path('booth_list', list_booth, name='list_booth'),

    path('booth/check_player', booth_home, name='booth_home'),


    path('booth/<str:booth_id>/', booth_home, name='booth_home'),
    path('booth/<str:booth_id>/check_player/<int:user_id>', check_player, name='check_player'),
    path('booth/<str:booth_id>/check_player', check_player, name='check_player'),
    path('booth/<str:booth_id>/register/<int:user_id>', register_player, name='register_player'),
    path('booth/traffics', list_booth, {"type": 'traffics'}, name='booth_traffics'),
    path('booth/participations', list_booth, {"type": 'participations'}, name='booth_participations'),
    path('booth/<str:booth_id>/participations', get_parti_record, name='booth_participations'),
    path('booth/<str:booth_id>/traffics', get_traffic_record, name='booth_traffic'),
    path('instructor', get_instructor_players, name='instructor_page'),
    path('instructor/register/<str:player_id>', register_instructor_comment, name='instructor_register')
]