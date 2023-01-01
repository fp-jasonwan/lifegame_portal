from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from booth.models import Booth, Participation, BoothScoring
from booth.forms import ParticipationForm
from account.models import User
from django.contrib import messages
from player.models import Player, InstructorScore
from player.views import get_profile
from player.forms import InstructorCommentForm
from .models import ContactPerson
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

def register(request):
    print(request.__dict__)
    return "Hi"

def register2(request):
    return HttpResponseRedirect()

def list_booth(request, type=""):
    booths = Booth.objects.filter(booth_admins__in=[request.user]).order_by('id')
    # profile = get_object_or_404(Student, user=request.user)
    if type == 'traffics':
        url_base = '/oc/booth/%s/traffics'
    elif type == 'participations':
        url_base = '/oc/booth/%s/participations'
    else:
        url_base = '/oc/booth/%s'

    if len(booths) > 1:
        template = loader.get_template('oc/booth_list.html')
        context = {
            'booths': booths,
            'url_base': url_base,
            'type': type
        }
        return HttpResponse(template.render(context, request))
    if len(booths) == 1:
        return redirect(url_base % (booths[0].id))
    else:
        return redirect('404')

def booth_home(request, booth_id):
    booth = get_object_or_404(Booth, id=booth_id)
    request.session['booth'] = booth.id
    template = loader.get_template('oc/booth_home.html')

    if request.method == 'POST':
        print(request.POST['is_active'] )
        booth.is_active = request.POST['is_active'] == 'true'
        booth.save()
    context = {
        'booth': booth
    }
    return HttpResponse(template.render(context, request))


def check_player(request, booth_id="", user_id=""):
    print(request)
    # booth = get_object_or_404(Booth, id=booth_id)
    # request.session['booth'] = booth.id
    # template = loader.get_template('oc/check_player.html')
    # context = {
    #     'booth': booth
    # }
    # print(user_id)
    # if user_id == "":
    #     return HttpResponse(template.render(context, request))
    # else:
    #     try:
    #         user = User.objects.get(id=user_id)
    #         print(hasattr(user, 'player'))
    #         if hasattr(user, 'player') == False:
    #             messages.success(request, '查無此玩家!')
    #             print('查無此玩家!')
    #             context['message'] = '查無此玩家!'
    #             return HttpResponse(template.render(context, request))
    #         player = user.player
    #     except:
    #         messages.success(request, '查無此玩家!')
    #         context['message'] = '查無此玩家!'
    #         return HttpResponse(template.render(context, request))
    #     return redirect('/oc/booth/{}/register/{}'.format(booth.id, user.id))
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
    request.session['from'] = request.META.get('HTTP_REFERER', '/')
    booth = get_object_or_404(Booth, id=booth_id)
    score_options = [option for option in booth.score_options.all()]
    user = get_object_or_404(User, id=user_id)
    if Participation.objects.filter(player=user.get_player(), booth=booth).exists():
        instance = Participation.objects.get(player=user.get_player(), booth=booth)
        form = ParticipationForm(request.POST or None, instance=instance)
    else:
        form = ParticipationForm(request.POST or None,
                                 initial={
                                     'booth': booth,
                                     'player': user.get_player(),
                                     'marker': request.user
                                 })
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '成功登記該玩家!')
            # return HttpResponseRedirect(f'/oc/booth/{booth.id}/traffics')
        else:
            print("INVALID FORM")
    template = loader.get_template('oc/booth_register.html')
    
    context = {
        'booth': booth,
        'user': user,
        'score_options': score_options,
        'form': form
    }
    return HttpResponse(template.render(context, request))

def get_instructor_players(request):
    instructor = request.user
    players = Player.objects.filter(instructor=instructor).all()
    for p in players:
        p.__dict__['comment_added'] = InstructorScore.objects.filter(player=p).count() > 0
    template = loader.get_template('oc/instructor.html')
    last_seen = Participation.objects.filter()
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


def get_contact(request):
    contacts = ContactPerson.objects.all()
    template = loader.get_template('contact.html')
    hall_link = request.user.hall_link
    context = {
        'contacts': contacts,
        'hall_link': hall_link
    }
    return HttpResponse(template.render(context, request))