from django.contrib import admin
from django.urls import path, include
from player.views import get_profile
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from news.views import NewsListView, get_news, get_news_content
from account.views import home_page
from booth.views import BoothsListView, get_booths_map
from oc.views import get_contact
from player.views import get_rich_list, get_score_list, get_instructor_students, instructor_get_player, get_map, show_participation, show_transaction, vote_best_booth

urlpatterns = [
    path('profile', get_profile, name='profile_by_userid'),
    path('profile/participation/<str:parti_id>', show_participation, name="get_participation_record"),
    path('profile/transaction/<str:tran_id>', show_transaction, name="get_tranasction_record"),

    path('', home_page, name='home'),
    path('oc/', include('oc.urls')),
    path('admin/', admin.site.urls),
    path('news/', get_news),
    path('news/<str:news_id>', get_news_content),
    path('contact/', get_contact, name='contact'),
    path('rich_list/', get_rich_list),
    path('score_list/', get_score_list),
    path('map/', get_map, name='map'),
    path('room/', TemplateView.as_view(template_name='room.html'), name='room'),
    path('rundown/', TemplateView.as_view(template_name='rundown.html'), name='rundown'),
    path('rules/', TemplateView.as_view(template_name='rules.html'), name='rules'),
    path('instructor/', get_instructor_students, name='instructor_students'),
    path('instructor/<str:player_id>', instructor_get_player, name='instructor_get_player'),

    path('instructor/<str:player_id>/participation/<str:parti_id>', show_participation, name="get_participation_record"),
    path('instructor/<str:player_id>/transaction/<str:tran_id>', show_transaction, name="get_tranasction_record"),
    path('vote', vote_best_booth, name='vote_booth'),
]