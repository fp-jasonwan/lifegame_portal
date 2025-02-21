from .views import oc_portal, search_profile, list_booth, booth_home,scan_player, check_player, register_page
from .views import redirect_to_booth, \
     update_booth_settings_requirement, booth_transaction, \
    update_booth_settings_scoring, create_booth_settings_scoring, kill_player, create_player
from .views import BoothParticipationView, BoothScoreFormView, get_register_score, show_booth_score, get_negative_steps_list
from django.urls import path, include
from django.contrib.auth.decorators import login_required, permission_required
from booth.views import show_participations, show_participation, \
                        delete_participation, show_transactions, show_transaction, delete_transaction
from player.views import show_participation as player_participation
from player.views import show_transaction as player_transaction

urlpatterns = [
    path('',oc_portal, name='oc_portal'),
    path('search_profile',search_profile, name='search_profile'),
    path('search_profile/<str:encrypted_id>', search_profile, name='search_profile_with_id'),
    path('search_profile/<str:encrypted_id>/transaction/<str:tran_id>', player_transaction, name='oc_player_transaction'),
    path('search_profile/<str:encrypted_id>/participation/<str:parti_id>', player_participation, name='oc_player_participation'),
    path('booth_list', list_booth, name='list_booth'),

    path('booth/check_player', booth_home, name='booth_home'),
    path('booth', redirect_to_booth, name='booth_home'),
    path('booth/<str:booth_id>/', booth_home, name='booth_home'),

    path('booth/<str:booth_id>/search_profile/<str:encrypted_id>', search_profile, name='booth_player_profile'),
    path('booth/<str:booth_id>/search_profile', search_profile, name='booth_search_profile'),
    path('booth/<str:booth_id>/check_player/<str:encrypted_id>', check_player, name='check_player'),
    path('booth/<str:booth_id>/check_player', scan_player, name='check_player'),
    path('booth/<str:booth_id>/register/<str:user_id>/option', get_register_score, name='register_option'),
    path('booth/<str:booth_id>/register/<str:user_id>', BoothParticipationView.as_view(), name='register_player'),
    # path('booth/<str:booth_id>/register2/<str:user_id>', BoothParticipationView.as_view(), name='register_player'),
    
    # Booth settings
    path('booth/<str:booth_id>/settings', show_booth_score, name='booth_setting'),
    path('booth/<str:booth_id>/settings/create', BoothScoreFormView.as_view(), name='booth_setting_score_create'),
    path('booth/<str:booth_id>/settings/<int:score_id>', BoothScoreFormView.as_view(), name='booth_setting_score'),
    # path('booth/<str:booth_id>/settings/<int:score_id>', update_booth_settings_scoring, name='update_booth_scoring'),
    # path('booth/<str:booth_id>/settings/create', create_booth_settings_scoring, name='create_booth_scoring'),


    path('booth/traffics', list_booth, {"type": 'traffics'}, name='booth_traffics'),
    path('booth/participations', list_booth, {"type": 'participations'}, name='booth_participations'),
    path('booth/<str:booth_id>/participations', show_participations, name='booth_participations'),
    path('booth/<str:booth_id>/participations/<str:parti_id>', show_participation, name='booth_participation'),
    path('booth/<str:booth_id>/participations/<str:parti_id>/success', show_participation, name='booth_participation_success'),
    path('booth/<str:booth_id>/participations/<str:parti_id>/delete', delete_participation, name='booth_participation_delete'),

    path('booth/<str:booth_id>/transactions', show_transactions, name='transaction_record'),
    path('booth/<str:booth_id>/transactions/<str:tran_id>', show_transaction, name='booth_transaction'),
    path('booth/<str:booth_id>/transactions/<str:tran_id>/success', show_transaction, name='transaction_record_success'),
    path('booth/<str:booth_id>/transactions/<str:tran_id>/delete', delete_transaction, name='transaction_record_success'),
    path('booth/<str:booth_id>/transaction/<str:type>', booth_transaction, name='transaction_scan'),
    path('booth/<str:booth_id>/transaction/<str:type>/<str:encrypted_id>', booth_transaction, name='transaction'),

    path('booth/<str:booth_id>/kill', kill_player, name='kill_player'),
    path('booth/<str:booth_id>/kill/<str:encrypted_id>', kill_player, name='kill_player'),
    
    path('booth/<str:booth_id>/create', create_player, name='create_player'),
    path('booth/<str:booth_id>/create/<str:encrypted_id>', create_player, name='create_player'),
    
    # path('instructor', get_instructor_players, name='instructor_page'),
    # path('instructor/register/<str:player_id>', register_instructor_comment, name='instructor_register'),

    path('booth/<str:booth_id>/negative_steps', get_negative_steps_list, name='negative_steps')
]