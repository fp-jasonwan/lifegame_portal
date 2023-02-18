from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Player, InstructorScore
from booth.models import Participation, BoothTraffic, Transaction
from django.shortcuts import get_object_or_404, render
import django_tables2 as tables
from account.models import User
from django_tables2 import SingleTableView
from django.db.models import Sum, Max, Subquery, Q
import pandas as pd
import datetime

# Create your views here.
def get_profile(request, user_id=""):
    if user_id == "":
        player = request.user.player
    else:
        user = User.objects.get(id=user_id)
        player = user.player
        # player = Player.objects.get(player_id=player_id)
    scores = player.get_scores()
    participations = Participation.objects.filter(player=player).all().order_by('-record_time')
    visits = BoothTraffic.objects.filter(player=player).all().order_by('-record_time')
    # instructor_score = InstructorScore.objects.filter(player=player).first()
    template = loader.get_template('player/profile.html')
    context = {
        'scores': scores,
        'player': player,
        'participations': participations,
        'visits': visits,
    }
    return HttpResponse(template.render(context, request))
    # return HttpResponse("You're voting on question %s." % question_id)
    

def get_profile_qrcode(request, user_id=""):
    if user_id == "":
        player = request.user.player
    else:
        user = User.objects.get(id=user_id)
        player = user.player
    profile_url = request.build_absolute_uri(f'/oc/search_profile/{user_id}')
    template = loader.get_template('player/profile_qrcode.html')
    context = {
        # 'scores': scores,
        'player': player,
        'profile_url': profile_url
    }
    return HttpResponse(template.render(context, request))

class PlayerParticipationTable(tables.Table):
    record_time = tables.DateTimeColumn(verbose_name= '時間', format='h:i A')
    booth = tables.Column(verbose_name='攤位')
    # overall_score = tables.Column(verbose_name='獲得分數', accessor='score.overall_score')
    class Meta:
        model = Participation
        template_name = "django_tables2/bootstrap.html"
        fields = ("record_time", "booth")
        sequence = ('record_time', 'booth', )
        attrs = {
            'class': 'table table-bordered dataTable'
        }

def get_rich_list(request):
    template = loader.get_template('ranking.html')
    rich_list_df = Player.get_rich_list()
    rich_list_df.rename(columns={'total_money': 'mark'}, inplace=True)
    context = {
        'list_name': '富豪榜',
        'mark_name': '金錢',
        'list': rich_list_df.head(10),
        'now': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return HttpResponse(template.render(context, request))

def get_score_list(request):
    template = loader.get_template('ranking.html')
    score_list_df = Player.get_total_score_list()
    score_list_df.rename(columns={'total_score': 'mark'}, inplace=True)
    context = {
        'list_name': '成就榜',
        'mark_name': '總分',
        'list': score_list_df.head(10),
        'now': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return HttpResponse(template.render(context, request))


# class PlayerParticipationListView(SingleTableView):
#     model = Participation
#     table_class = PlayerParticipationTable
#     template_name = 'news.html'
 