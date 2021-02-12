from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Player
from django.shortcuts import get_object_or_404, render
# Create your views here.

def get_profile(request, player_id=""):
    print(player_id)
    if player_id == "":
        player = request.user.player
        scores = player.get_scores()
        print(scores)
        # profile = get_object_or_404(Student, user=request.user)
        template = loader.get_template('player/profile.html')
        context = {
            'scores': scores,
            'player': player,
        }
        return HttpResponse(template.render(context, request))
    # return HttpResponse("You're voting on question %s." % question_id)