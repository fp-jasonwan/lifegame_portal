from django.shortcuts import render, redirect

# Create your views here.
from django_tables2 import SingleTableView
from .models import Booth, Participation, BoothTraffic

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


def get_booths_map(request):
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
        'booth_dict': booth_dict
    }
    return HttpResponse(template.render(context, request))

def redirect_zoom(request, booth_id):
    request.session['from'] = request.META.get('HTTP_REFERER', '/')
    booth = Booth.objects.get(id=booth_id)
    if request.user.is_player():
        if booth.is_active:
            traffic = BoothTraffic(
                booth = booth,
                player = request.user.get_player()
            )
            traffic.save()
            response = redirect(booth.url)
            return response
        else:

            messages.error(request, '此攤位已經爆滿!')
            return HttpResponseRedirect("/booths")
    else:
        response = redirect(booth.url)
        return response


class TrafficTable(tables.Table):
    def __init__(self, *args, **kwargs):
        if kwargs.pop("booth", False):
            for column in self.base_columns.values():
                if isinstance(column, tables.LinkColumn):
                    column.args.insert(0, "booth")
        super(TrafficTable, self).__init__(*args, **kwargs)

    player = tables.TemplateColumn('<a href="/oc/search_profile/{{record.player.user.id }}">{{record.player}}</a>',
                                   verbose_name='玩家')
    record_time = tables.DateTimeColumn(verbose_name='時間', format='h:i A')
    register = tables.TemplateColumn('<a href="/oc/booth/{{booth.booth_id }}">{{record.player}}</a>',
                                   verbose_name='登記')

    class Meta:
        model = BoothTraffic
        template_name = "django_tables2/bootstrap.html"
        fields = ("player", "record_time", "register")
        attrs = {
            'class': 'table table-bordered dataTable'
        }


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

def get_parti_record(request, booth_id):
    booth = Booth.objects.get(id=booth_id)
    participations = Participation.objects.filter(booth=booth).all().order_by('-record_time')
    template = loader.get_template('oc/booth_participations.html')
    context = {
        'booth': booth,
        'participations': participations,

    }
    return HttpResponse(template.render(context, request))


def get_traffic_record(request, booth_id):
    booth = Booth.objects.get(id=booth_id)
    traffic = BoothTraffic.objects.filter(
        booth=booth
    ).all().order_by('-record_time')
    template = loader.get_template('oc/booth_traffic.html')
    context = {
        'booth': booth,
        'traffic': traffic,
    }
    return HttpResponse(template.render(context, request))