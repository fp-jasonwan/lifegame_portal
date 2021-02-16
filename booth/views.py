from django.shortcuts import render

# Create your views here.
from django_tables2 import SingleTableView
from .models import Booth, Participation

from django.http import HttpResponse
import django_tables2 as tables
from django.template import loader
class BoothsTable(tables.Table):
    name = tables.TemplateColumn('<a href="{{record.booth.url}}">{{record.booth}}</a>', verbose_name='攤位')    
    description = tables.Column(verbose_name='簡介', accessor='booth.description')
    # description = tables.TemplateColumn('{{ record.booth.description|linebreaks }}', verbose_name='簡介')
    class Meta:
        model = Booth
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "description")
        attrs = {
            'class': 'table table-bordered dataTable'
        }

class BoothsListView(SingleTableView):
    model = Participation
    table_class = BoothsTable
    template_name = 'booths.html'

class ParticipationsTable(tables.Table):
    
    record_time = tables.DateTimeColumn(verbose_name= '時間', format='h:i A')
    player = tables.TemplateColumn('<a href="/oc/search_profile/{{record.player.id }}">{{record.player}}</a>', verbose_name='玩家')    
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
    participations = Participation.objects.filter(booth=booth).all()
    template = loader.get_template('oc/booth_participations.html')
    context = {
        'participations': ParticipationsTable(participations),

    }
    return HttpResponse(template.render(context, request))