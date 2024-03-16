from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Player, InstructorScore
from booth.models import Participation, BoothTraffic, Transaction
from news.models import News, NewsCategory
from django.shortcuts import get_object_or_404, render
import django_tables2 as tables
from account.models import User, InstructorGroup
from django_tables2 import SingleTableView
from django.db.models import Sum, Max, Subquery, Q
import pandas as pd
from constance import config
import datetime
from urllib.parse import urlparse
from .forms import BoothSettingsForm

# Create your views here.
def get_profile(request, encrypted_id=""):
    user = get_object_or_404(User, encrypted_id=encrypted_id)
    player = user.player
    if player:
        scores = player.get_scores()
        participations = Participation.objects.filter(player=player).all().order_by('-record_time')
        transactions = Transaction.objects.filter(player=player).all().order_by('-record_time')
        visits = BoothTraffic.objects.filter(player=player).all().order_by('-record_time')
        # instructor_score = InstructorScore.objects.filter(player=player).first()
        template = loader.get_template('player/profile.html')
        print(scores['steps'])
        context = {
            'encrypted_id': encrypted_id,
            'scores': scores,
            'player': player,
            'participations': participations,
            'transactions': transactions,
            'visits': visits,
        }
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('error/error_message.html')
        context = {
            "message": f"{config.DEATH_MESSAGE_1}，{config.DEATH_MESSAGE_2}"
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
    rich_list_df.rename(columns={'money': 'mark'}, inplace=True)
    print(rich_list_df.head(10))
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

def get_map(request, encrypted_id=""):
    template = loader.get_template('map.html')
    news_categories = NewsCategory.objects.all()
    context = {
        'news_categories': news_categories,
        'encrypted_id': encrypted_id,
    }
    return HttpResponse(template.render(context, request))

def get_instructor_students(request, encrypted_id=""):
    user = get_object_or_404(User, encrypted_id=encrypted_id)
    template = loader.get_template('instructor_students.html')
    if user.user_type == 'instructor':
        group = get_object_or_404(InstructorGroup, instructor=user)
        context = {
            'group_id': group.id,
            'students': group.students.order_by('id').all(),
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
    

def show_participation(request, parti_id, encrypted_id=""):
    template = loader.get_template('player/booth_participation.html')
    participation = get_object_or_404(Participation, id=parti_id)
    scores = {}
    for s in ['health_score','skill_score','growth_score','relationship_score','money', 'academic_level','steps','flat']:
        if getattr(participation.score, s) != 0:
            field_name = participation.score._meta.get_field(s).verbose_name
            scores[field_name] = getattr(participation.score, s)
    print(scores )
    context = {
        'participation': participation,
        'scores': scores
    }
    return HttpResponse(template.render(context, request))

def show_transaction(request, tran_id, encrypted_id=""):
    template = loader.get_template('player/booth_transaction.html')
    transaction = get_object_or_404(Transaction, id=tran_id)
    transaction_record = {}
    if transaction.get_money() != 0:
        transaction_record['金錢'] = transaction.get_money()
    if transaction.get_deposit() != 0:
        transaction_record['銀行存款'] = transaction.get_deposit()
    if transaction.interest_rate != 0:
        transaction_record['利率'] = transaction.interest_rate()
    context = {
        'transaction': transaction,
        'scores': transaction_record,
    }
    return HttpResponse(template.render(context, request))

def instructor_get_player(request, encrypted_id, player_id):
    instructor = get_object_or_404(User, encrypted_id=encrypted_id)
    group = get_object_or_404(InstructorGroup, instructor=instructor)
    player = get_object_or_404(Player, id=player_id)
    scores = player.get_scores()
    participations = Participation.objects.filter(player=player).all().order_by('-record_time')
    transactions = Transaction.objects.filter(player=player).all().order_by('-record_time')
    visits = BoothTraffic.objects.filter(player=player).all().order_by('-record_time')
    template = loader.get_template('player/profile.html')
    context = {
        'group_id': group.id,
        'encrypted_id': encrypted_id,
        'scores': scores,
        'player': player,
        'participations': participations,
        'transactions': transactions,
        'visits': visits,
        'is_instructor': True
    }
    return HttpResponse(template.render(context, request))
    
def vote_best_booth(request, encrypted_id=""):
    user = User.objects.get(encrypted_id=encrypted_id)
    request.session['from'] = request.META.get('HTTP_REFERER', '/')
    # if Booth.objects.filter(booth=booth).exists():
    instance = user
    form = BoothSettingsForm(request.POST or None, instance=instance)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            msg_template = loader.get_template('player/player_message.html')
            context = {
                'encrypted_id': encrypted_id,
                'message': '成功投選我最喜愛攤位!'
            }
            return HttpResponse(msg_template.render(context, request))
        else:
            print("INVALID FORM")
    template = loader.get_template('player/voting_booth.html')
    
    context = {
        'encrypted_id': encrypted_id,
        'form': form,
        'user': user,
    }
    return HttpResponse(template.render(context, request))

# def create_player(request, encrypted_id):
