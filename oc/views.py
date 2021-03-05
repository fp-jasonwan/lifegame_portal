from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import loader
from booth.models import Booth, Participation, BoothScoring
from booth.forms import ParticipationForm
from account.models import User
from django.contrib import messages
from player.models import Player, InstructorScore
from player.views import get_profile
from player.forms import InstructorCommentForm
# Create your views here.
# Create your views here.

def oc_portal(request):
    if request.user.is_authenticated == False:
        return redirect('/')
    if request.user.user_type == 'student':
        return redirect('/404')
    return render(request, 'oc/oc_portal.html')

def search_profile(request, user_id=""):
    # profile = get_object_or_404(Student, user=request.user)
    template = loader.get_template('oc/search_profile.html')
    context = {
    }
    if user_id == "":
        return HttpResponse(template.render(context, request))
    else:
        
        print('check point 1', user_id)
        try:
            user = User.objects.get(id=user_id)
            print(hasattr(user, 'player'))
            if hasattr(user, 'player') == False:
                messages.success(request, '查無此玩家!')
                context['message'] = '查無此玩家!'
                return HttpResponse(template.render(context, request))
            player = user.player
        except:
            messages.success(request, '查無此玩家!')
            context['message'] = '查無此玩家!'
            return HttpResponse(template.render(context, request))
        print(user_id)
        return get_profile(request, user_id)
        # return redirect('/oc/booth/{}/register/{}'.format(booth.id, user.id))
    return HttpResponse(template.render(context, request))
    # return HttpResponse("You're voting on question %s." % question_id)


def list_booth(request):
    booths = Booth.objects.filter(booth_admins__in=[request.user]).order_by('id')
    # profile = get_object_or_404(Student, user=request.user)
    if len(booths) > 1:
        template = loader.get_template('oc/booth_list.html')
        context = {
            'booths': booths
        }
        return HttpResponse(template.render(context, request))
    if len(booths) == 1:
        return redirect('/oc/booth/{}'.format(booths[0].id))
    else:
        return redirect('404')

def booth_home(request, booth_id):
    booth = get_object_or_404(Booth, id=booth_id)
    request.session['booth'] = booth.id
    template = loader.get_template('oc/booth_home.html')
    context = {
        'booth': booth
    }
    return HttpResponse(template.render(context, request))

def check_player(request, booth_id, user_id=""):
    booth = get_object_or_404(Booth, id=booth_id)
    request.session['booth'] = booth.id
    template = loader.get_template('oc/check_player.html')
    context = {
        'booth': booth
    }
    print(user_id)
    if user_id == "":
        return HttpResponse(template.render(context, request))
    else:
        try:
            user = User.objects.get(id=user_id)
            print(hasattr(user, 'player'))
            if hasattr(user, 'player') == False:
                messages.success(request, '查無此玩家!')
                print('查無此玩家!')
                context['message'] = '查無此玩家!'
                return HttpResponse(template.render(context, request))
            player = user.player
        except:
            messages.success(request, '查無此玩家!')
            context['message'] = '查無此玩家!'
            return HttpResponse(template.render(context, request))
        return redirect('/oc/booth/{}/register/{}'.format(booth.id, user.id))
        # else:
        #     context['message'] = '此玩家不符合資格!'
        # return HttpResponse(template.render(context, request))

def register_page(request, booth_id, user_id):
    booth = get_object_or_404(Booth, id=booth_id)
    score_options = [option for option in booth.score_options.all()]
    user = get_object_or_404(User, id=user_id)
    template = loader.get_template('oc/booth_register.html')
    
    context = {
        'booth': booth,
        'user': user,
        'score_options': score_options
    }
    return HttpResponse(template.render(context, request))

def register_player(request, booth_id, user_id, participation=""):
    booth = get_object_or_404(Booth, id=booth_id)
    score_options = [option for option in booth.score_options.all()]
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = ParticipationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print("VALID FORM")
            booth_score_id = form.cleaned_data['booth_score_id']
            remarks = form.cleaned_data['remarks']
            booth_score = BoothScoring.objects.get(id=booth_score_id)
            new_parti = Participation(
                booth = booth, 
                player=user.player, 
                score=booth_score, 
                remarks=remarks,
                marker = request.user
            )
            new_parti.save()
            messages.success(request, '成功登記該玩家!')
        else:
            print("INVALID FORM")
    template = loader.get_template('oc/booth_register.html')
    
    context = {
        'booth': booth,
        'user': user,
        'score_options': score_options
    }
    return HttpResponse(template.render(context, request))

def get_instructor_players(request):
    instructor = request.user
    players = Player.objects.filter(instructor=instructor).all()
    for p in players:
        print(p)
        print(InstructorScore.objects.filter(player=p).count())
        p.__dict__['comment_added'] = InstructorScore.objects.filter(player=p).count() > 0
    template = loader.get_template('oc/instructor.html')
    context = {
        'players': players,
    }
    return HttpResponse(template.render(context, request))

def register_instructor_comment(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    try:
        comment_record = InstructorScore.objects.get(player=player)
    except:
        comment_record = None
    if request.method == 'POST':
        print(request.POST)
        form = InstructorCommentForm(request.POST)
        if form.is_valid():
            print("VALID FORM")
            comments = form.cleaned_data['comments']
            score = form.cleaned_data['score']

            if not comment_record:
                comment_record = InstructorScore(
                    player = player, 
                    score=score, 
                    comments=comments,
                    instructor=request.user, 
                )
            comment_record.save()
            messages.success(request, '評分已被記錄!')
        else:
            print("INVALID FORM")
    template = loader.get_template('oc/instructor_comment.html')
    
    context = {
        'player': player,
        'comment': comment_record
    }
    return HttpResponse(template.render(context, request))
