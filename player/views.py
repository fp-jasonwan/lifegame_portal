from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Player, InstructorScore
from booth.models import Participation, BoothTraffic
from django.shortcuts import get_object_or_404, render
import django_tables2 as tables
from account.models import User

# Create your views here.

def get_profile(request, user_id=""):
    if user_id == "":
        player = request.user.player
    else:
        user = User.objects.get(id=user_id)
        player = user.player
        # player = Player.objects.get(player_id=player_id)
    # scores = player.get_scores()
    participations = Participation.objects.filter(player=player).all().order_by('-record_time')
    visits = BoothTraffic.objects.filter(player=player).all().order_by('-record_time')
    # instructor_score = InstructorScore.objects.filter(player=player).first()
    template = loader.get_template('player/profile.html')
    context = {
        # 'scores': scores,
        'player': player,
        'participations': participations,
        'visits': visits,
        # 'instructor_score': instructor_score
    }
    return HttpResponse(template.render(context, request))
    # return HttpResponse("You're voting on question %s." % question_id)

class PlayerParticipationTable(tables.Table):
    record_time = tables.DateTimeColumn(verbose_name= '時間', format='h:i A')
    booth = tables.Column(verbose_name='攤位')
    overall_score = tables.Column(verbose_name='獲得分數', accessor='score.overall_score')
    class Meta:
        model = Participation
        template_name = "django_tables2/bootstrap.html"
        fields = ("record_time", "booth")
        sequence = ('record_time', 'booth', )
        attrs = {
            'class': 'table table-bordered dataTable'
        }


# class PlayerParticipationListView(SingleTableView):
#     model = Participation
#     table_class = PlayerParticipationTable
#     template_name = 'news.html'
