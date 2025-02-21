from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
from django_tables2 import SingleTableView
from .models import Booth, Participation, Transaction
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
import django_tables2 as tables
from django.template import loader

class BoothsTable(tables.Table):
    name = tables.TemplateColumn('<a href="{{record.url}}">{{record}}</a>', verbose_name='攤位')    
    # description = tables.Column(verbose_name='簡介', accessor='booth.description')
    description = tables.TemplateColumn('{{ record.description|linebreaks }}', verbose_name='簡介')
    class Meta:
        model = Booth
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "description")
        attrs = {
            'class': 'table table-bordered dataTable'
        }

class BoothsListView(SingleTableView):
    model = Booth
    table_class = BoothsTable
    template_name = 'booths.html'


def get_booths_map(request, encrypted_id=""):
    booths = Booth.objects.all()
    categories = [b.description for b in booths]
    categories = list(set(categories))
    booth_dict = {
        'OLE': [],
        'Non-OLE': [],
        '工作分享': [],
        '升學': []
    }
    # for cat in sorted(categories):
    #     booth_dict[cat] = []
    for b in booths:
        if b.id[0] == 'O':
            booth_dict['OLE'].append(b)
        elif b.id[0] == 'N':
            booth_dict['Non-OLE'].append(b)
        elif b.id[0] == 'E':
            booth_dict['升學'].append(b)
        elif b.id[0] == 'J':
            booth_dict['工作分享'].append(b)
    template = loader.get_template('booths.html')
    context = {
        # 'booths': booths,
        'categories': categories,
        'booth_dict': booth_dict,
        'encrypted_id': encrypted_id
    }
    return HttpResponse(template.render(context, request))


class ParticipationsTable(tables.Table):
    
    record_time = tables.DateTimeColumn(verbose_name= '時間', format='h:i A')
    player = tables.TemplateColumn('<a href="/oc/search_profile/{{record.player.user.id }}">{{record.player}}</a>', verbose_name='玩家')    
    class Meta:
        model = Participation
        template_name = "django_tables2/bootstrap.html"
        fields = ("record_time", "player", "score")
        attrs = {
            'class': 'table table-bordered dataTable'
        }

class ParticipationsListView(SingleTableView):
    model = Participation
    table_class = ParticipationsTable
    template_name = 'booths.html'

def show_participations(request, booth_id):
    booth = Booth.objects.get(id=booth_id)
    participations = Participation.objects.filter(booth=booth).all().order_by('-record_time')
    template = loader.get_template('oc/booth_participations.html')
    context = {
        'booth': booth,
        'participations': participations,

    }
    return HttpResponse(template.render(context, request))

def show_transactions(request, booth_id):
    booth = Booth.objects.get(id=booth_id)
    transactions = Transaction.objects.filter(booth=booth).all().order_by('-record_time')
    template = loader.get_template('oc/booth_transactions.html')
    context = {
        'booth': booth,
        'transactions': transactions,
    }
    return HttpResponse(template.render(context, request))


def show_participation(request, booth_id=None, parti_id=None, message=""):
    if 'success' in request.path:
        message = '成功登記玩家！'
    template = loader.get_template('oc/booth_participation.html')
    booth = get_object_or_404(Booth, id=booth_id)
    participation = get_object_or_404(Participation, id=parti_id)
    score_list = {
        '健康指數': participation.health_score,
        '技能指數': participation.skill_score,
        '成長指數': participation.growth_score,
        '關係指數': participation.relationship_score,
        '金錢': participation.money,
        '學業': participation.academic_level,
        '步數': participation.steps,
        '樓宇': participation.flat
    }
    print(score_list)
    context = {
        'message': message, 
        'booth': booth,
        'participation': participation,
        'score_list': score_list
    }
    return HttpResponse(template.render(context, request))

def delete_participation(request, booth_id, parti_id):
    Participation.objects.get(id=parti_id).delete()
    booth = Booth.objects.get(id=booth_id)
    template = loader.get_template('oc/booth_message.html')
    context = {
        'booth': booth,
        "message": "參與記錄已被刪除"
    }
    return HttpResponse(template.render(context, request))


def show_transaction(request, booth_id, tran_id, message=""):
    if 'success' in request.path:
        message = '成功登記玩家！'
    template = loader.get_template('oc/booth_transaction.html')
    booth = get_object_or_404(Booth, id=booth_id)
    transaction = get_object_or_404(Transaction, id=tran_id)
    context = {
        'message': message, 
        'booth': booth,
        'transaction': transaction
    }
    return HttpResponse(template.render(context, request))

def delete_transaction(request, booth_id, tran_id):
    Transaction.objects.get(id=tran_id).delete()
    booth = Booth.objects.get(id=booth_id)
    template = loader.get_template('oc/booth_message.html')
    context = {
        'booth': booth,
        "message": "參與記錄已被刪除"
    }
    return HttpResponse(template.render(context, request))