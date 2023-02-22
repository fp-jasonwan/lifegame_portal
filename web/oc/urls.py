from .views import oc_portal, search_profile, list_booth, booth_home,scan_player, check_player, register_player, register_page, get_instructor_players, register_instructor_comment
from .views import redirect_to_booth, update_booth_settings, booth_transaction
from django.urls import path, include
from django.contrib.auth.decorators import login_required, permission_required
from booth.views import show_participations, get_traffic_record, show_participation, \
                        delete_participation, show_transactions, show_transaction, delete_transaction

urlpatterns = [
    path('',oc_portal, name='oc_portal'),
    path('search_profile',search_profile, name='search_profile'),
    path('search_profile/<str:encrypted_id>', search_profile, name='search_profile_with_id'),
    path('booth_list', list_booth, name='list_booth'),

    path('booth/check_player', booth_home, name='booth_home'),
    path('booth', redirect_to_booth, name='booth_home'),
    path('booth/<str:booth_id>/', booth_home, name='booth_home'),
    path('booth/<str:booth_id>/check_player/<str:encrypted_id>', check_player, name='check_player'),
    path('booth/<str:booth_id>/check_player', scan_player, name='check_player'),
    path('booth/<str:booth_id>/register/<str:encrypted_id>', register_player, name='register_player'),
    path('booth/<str:booth_id>/settings', update_booth_settings, name='update_booth_settings'),
    path('booth/traffics', list_booth, {"type": 'traffics'}, name='booth_traffics'),
    path('booth/participations', list_booth, {"type": 'participations'}, name='booth_participations'),
    path('booth/<str:booth_id>/participations', show_participations, name='booth_participations'),
    path('booth/<str:booth_id>/participations/<str:parti_id>', show_participation, name='booth_participation'),
    path('booth/<str:booth_id>/participations/<str:parti_id>/success', show_participation, name='booth_participation_success'),
    path('booth/<str:booth_id>/participations/<str:parti_id>/delete', delete_participation, name='booth_participation_delete'),
    path('booth/<str:booth_id>/traffics', get_traffic_record, name='booth_traffic'),

    path('booth/<str:booth_id>/transactions', show_transactions, name='transaction_record'),
    path('booth/<str:booth_id>/transactions/<str:tran_id>', show_transaction, name='transaction_record'),
    path('booth/<str:booth_id>/transactions/<str:tran_id>/success', show_transaction, name='transaction_record_success'),
    path('booth/<str:booth_id>/transactions/<str:tran_id>/delete', delete_transaction, name='transaction_record_success'),
    path('booth/<str:booth_id>/transaction/<str:type>', booth_transaction, name='transaction_scan'),
    path('booth/<str:booth_id>/transaction/<str:type>/<str:encrypted_id>', booth_transaction, name='transaction'),
    
    path('instructor', get_instructor_players, name='instructor_page'),
    path('instructor/register/<str:player_id>', register_instructor_comment, name='instructor_register')
]