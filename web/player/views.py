from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Player, InstructorScore
from booth.models import Participation, BoothTraffic, Transaction
from django.shortcuts import get_object_or_404, render
import django_tables2 as tables
from account.models import User, InstructorGroup
from django_tables2 import SingleTableView
from django.db.models import Sum, Max, Subquery, Q
import pandas as pd
import datetime

# Create your views here.
def get_profile(request, encrypted_id=""):
    user = get_object_or_404(User, encrypted_id=encrypted_id)
    player = user.player
    if player:
        scores = player.get_scores()
        participations = Participation.objects.filter(player=player).all().order_by('-record_time')
        visits = BoothTraffic.objects.filter(player=player).all().order_by('-record_time')
        # instructor_score = InstructorScore.objects.filter(player=player).first()
        template = loader.get_template('player/profile.html')
        context = {
            'encrypted_id': encrypted_id,
            'scores': scores,
            'player': player,
            'participations': participations,
            'visits': visits,
        }
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('error/error_message.html')
        context = {
            "message": "玩家的角色已經死亡／失效，請到大禮堂"
        }
        return HttpResponse(template.render(context, request))

    # return HttpResponse("You're voting on question %s." % question_id)
    

def get_profile_qrcode(request, encrypted_id=""):
    if encrypted_id == "":
        player = request.user.player
    else:
        user = User.objects.get(encrypted_id=encrypted_id)
        player = user.player
    profile_url = request.build_absolute_uri(f'/oc/search_profile/{encrypted_id}')
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

def get_rich_list(request, encrypted_id=""):
    template = loader.get_template('ranking.html')
    rich_list_df = Player.get_rich_list()
    rich_list_df.rename(columns={'total_money': 'mark'}, inplace=True)
    context = {
        'list_name': '富豪榜',
        'mark_name': '金錢',
        'list': rich_list_df.head(10),
        'encrypted_id': encrypted_id,
        'now': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return HttpResponse(template.render(context, request))

def get_score_list(request, encrypted_id=""):
    template = loader.get_template('ranking.html')
    score_list_df = Player.get_total_score_list()
    score_list_df.rename(columns={'total_score': 'mark'}, inplace=True)
    context = {
        'list_name': '成就榜',
        'mark_name': '總分',
        'encrypted_id': encrypted_id,
        'list': score_list_df.head(10),
        'now': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return HttpResponse(template.render(context, request))

def get_instructor_students(request, encrypted_id=""):
    user = get_object_or_404(User, encrypted_id=encrypted_id)
    template = loader.get_template('instructor_students.html')
    if user.user_type == 'instructor':
        group = get_object_or_404(InstructorGroup, instructor=user)
        context = {
            'group_id': group.id,
            'students': group.students.all(),
            'players': group.get_player(),
            'encrypted_id': encrypted_id
        }
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('error/error_message.html')
        context = {
            "message": "此用戶並不是導師。如有錯誤請聯絡IT小組"
        }
        return HttpResponse(template.render(context, request))
    

def instructor_get_player(request, encrypted_id, player_id):
    instructor = get_object_or_404(User, encrypted_id=encrypted_id)
    group = get_object_or_404(InstructorGroup, instructor=instructor)
    player = get_object_or_404(Player, id=player_id)
        # player = Player.objects.get(player_id=player_id)
    scores = player.get_scores()
    participations = Participation.objects.filter(player=player).all().order_by('-record_time')
    visits = BoothTraffic.objects.filter(player=player).all().order_by('-record_time')
    # instructor_score = InstructorScore.objects.filter(player=player).first()
    template = loader.get_template('player/profile.html')
    context = {
        'group_id': group.id,
        'encrypted_id': encrypted_id,
        'scores': scores,
        'player': player,
        'participations': participations,
        'visits': visits,
        'is_instructor': True
    }
    return HttpResponse(template.render(context, request))