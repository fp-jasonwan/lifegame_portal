from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from booth.models import Booth, Participation, BoothScoring, Transaction, BoothTraffic
from booth.forms import ParticipationForm, BoothSettingsForm, TransactionForm
from account.models import User
from django.contrib import messages
from player.models import Player, InstructorScore
from player.views import get_profile
from player.forms import InstructorCommentForm
from .models import ContactPerson
from booth.views import show_participation
from django.db.models import Q
# Create your views here.
# Create your views here.
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
import datetime

def access_checking(request):
    if request.user.is_oc() == False:
        msg_template = loader.get_template('error/error_message.html')
        context = {
            'error_type': 'access_denied',
            'message': 'Access denied!'
        }
        return HttpResponse(msg_template.render(context, request))

def oc_portal(request):
    if request.user.is_authenticated == False:
        return redirect('/accounts/login?next=/oc/booth')
    if request.user.user_type == 'student':
        return redirect('/404')
    return render(request, 'oc/home.html')

def search_profile(request, encrypted_id=""):
    access_checking(request)

    # profile = get_object_or_404(Student, user=request.user)
    template = loader.get_template('oc/search_profile.html')
    context = {
    }
    if encrypted_id == "":
        return HttpResponse(template.render(context, request))
    else:
        try:
            if encrypted_id.isnumeric():
                user = get_object_or_404(User, id=int(encrypted_id))
                player = user.player
            elif len(encrypted_id) < 10:
                id = int(encrypted_id[:3])
                user = get_object_or_404(User, id=id)
                player = user.player
            else:
                user = get_object_or_404(User, encrypted_id=encrypted_id)
                player = user.player
        except:
            messages.success(request, '查無此玩家!')
            context['message'] = '查無此玩家!'
            return HttpResponse(template.render(context, request))
        scores = player.get_scores()
        participations = Participation.objects.filter(player=player).all().order_by('-record_time')
        # instructor_score = InstructorScore.objects.filter(player=player).first()
        template = loader.get_template('player/profile.html')
        context = {
            'scores': scores,
            'player': player,
            'participations': participations,
        }
        return HttpResponse(template.render(context, request))
        # return get_profile(request, encrypted_id)
        # return redirect('/oc/booth/{}/register/{}'.format(booth.id, user.id))
    return HttpResponse(template.render(context, request))
    # return HttpResponse("You're voting on question %s." % question_id)


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

def scan_player(request, booth_id):
    booth = get_object_or_404(Booth, id=booth_id)
    template = loader.get_template('oc/check_player.html')
    context = {
        'booth': booth,
        'type': 'check'
    }
    return HttpResponse(template.render(context, request))

def check_player(request, booth_id="", encrypted_id=""):
    print('checkpoint 1: ', datetime.datetime.now())
    booth = get_object_or_404(Booth, id=booth_id)
    if encrypted_id.isnumeric():
        user = get_object_or_404(User, id=encrypted_id)
    else:
        user = get_object_or_404(User, encrypted_id=encrypted_id)
    print('checkpoint 2: ', datetime.datetime.now())
    player = user.player
    request.session['booth'] = booth.id
    score_translation = {
        'health_score': '健康',
        'skill_score': '健康',
        'growth_score': '成長',
        'relationship_score': '健康',
        'money': '金錢'
    }
    msg_template = loader.get_template('oc/booth_message.html')
    context = {
        'booth': booth,
        'booth_scores': booth.get_requirements(),
        'player_scores': player.get_scores(),
        'score_translation': score_translation,
        'score_types': ['health_score', 'skill_score', 'growth_score', 'relationship_score', 'money']
    }

    # If the user does not exist, return error
    if hasattr(user, 'player') == False:
        context['error_type'] = 'unknown_user'
        context['message'] = '查無此玩家!'
        return HttpResponse(msg_template.render(context, request))
    
    # Check player eligibility
    print('checkpoint 3: ', datetime.datetime.now())
    eligibility = booth.check_player(player)
    print('checkpoint 4: ', datetime.datetime.now())
    if len(eligibility) == 0:
        return redirect('/oc/booth/{}/register/{}'.format(booth.id, user.id)) 
    else:
        context['eligibility'] = eligibility
        context['error_type'] = 'not_eligible'
        context['message'] = '此玩家不符合攤位要求!'
        return HttpResponse(msg_template.render(context, request))

def register_page(request, booth_id, encrypted_id):
    booth = get_object_or_404(Booth, id=booth_id)
    score_options = [option for option in booth.score_options.all()]
    print(score_options)
    if encrypted_id.isnumeric():
        user = get_object_or_404(User, id=encrypted_id)
    else:
        user = get_object_or_404(User, encrypted_id=encrypted_id)
    template = loader.get_template('oc/booth_register.html')
    
    context = {
        'booth': booth,
        'user': user,
        'score_options': score_options
    }
    return HttpResponse(template.render(context, request))

def register_player(request, booth_id, encrypted_id, participation=""):
    request.session['from'] = request.META.get('HTTP_REFERER', '/')
    booth = get_object_or_404(Booth, id=booth_id)
    score_options = [option for option in booth.score_options.all()]

    print('register checkpoint 1: ', datetime.datetime.now())
    if encrypted_id.isnumeric():
        user = get_object_or_404(User, id=encrypted_id)
    else:
        user = get_object_or_404(User, encrypted_id=encrypted_id)
    
    print('register checkpoint 2: ', datetime.datetime.now())
    player = user.get_player()
    form = ParticipationForm(request.POST or None,
                                initial={
                                    'booth': booth,
                                    'player': player,
                                    'marker': request.user
                                })
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            player = form.cleaned_data['player']
            booth = form.cleaned_data['booth']
            participation = Participation.objects.filter(
                booth=booth,
                player=player
            ).order_by('-record_time')[0]
            return HttpResponseRedirect(f'/oc/booth/{booth.id}/participations/{participation.id}/success')
        else:
            print("INVALID FORM")
    template = loader.get_template('oc/booth_register2.html')
    print('register checkpoint 3: ', datetime.datetime.now())

    # reduce options in the fields
    form.fields['booth'].queryset = Booth.objects.filter(id=booth.id)
    form.fields['player'].queryset = Player.objects.filter(id=player.id)
    form.fields['marker'].queryset = User.objects.filter(id=request.user.id)
    context = {
        'action_path': 'register', 
        'booth': booth,
        'player': player,
        'marker': request.user,
        'score_options': score_options,
        'form': form
    }
    print('register checkpoint 4: ', datetime.datetime.now())
    return HttpResponse(template.render(context, request))


def update_booth_settings(request, booth_id):
    request.session['from'] = request.META.get('HTTP_REFERER', '/')
    booth = get_object_or_404(Booth, id=booth_id)
    # if Booth.objects.filter(booth=booth).exists():
    instance = booth
    form = BoothSettingsForm(request.POST or None, instance=instance)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            msg_template = loader.get_template('oc/booth_message.html')
            context = {
                'booth': booth,
                'message': '成功更新攤位要求!'
            }
            return HttpResponse(msg_template.render(context, request))
        else:
            print("INVALID FORM")
    template = loader.get_template('oc/booth_settings.html')
    
    context = {
        'booth': booth,
        'form': form
    }
    return HttpResponse(template.render(context, request))


def booth_transaction(request, booth_id, type, encrypted_id=""):
    booth = get_object_or_404(Booth, id=booth_id)
    if encrypted_id == "":
        template = loader.get_template('oc/check_player.html')
        context = {
            'booth': booth,
            'scan_type': type
        }
        return HttpResponse(template.render(context, request))
    else:
        request.session['from'] = request.META.get('HTTP_REFERER', '/')
        try:
            if encrypted_id[:3].isnumeric():
                user = get_object_or_404(User, id=encrypted_id[:3])
            else:
                user = get_object_or_404(User, encrypted_id=encrypted_id)
        except:
            template = loader.get_template('oc/booth_message.html')
            context = {
                'booth': booth,
                'message': '查無此玩家!'
            }
            return HttpResponse(template.render(context, request))
        form = TransactionForm(request.POST or None,
                                    initial={
                                        'booth': booth,
                                        'player': user.get_player(),
                                        'marker': request.user,
                                        'type': type
                                    })
        if request.method == 'POST':
            if form.is_valid():
                # Check balance
                player = form.cleaned_data['player']
                booth = form.cleaned_data['booth']
                type = form.cleaned_data['type']
                money = form.cleaned_data['money']
                player_money = player.get_score('money')
                if type == 'receive':
                    if money > player_money:
                        msg_template = loader.get_template('oc/booth_message.html')
                        context = {
                            'error_type': 'insufficient_amount',
                            'message': f"""
                                玩家金錢不足! 玩家現有金錢為${player_money} < 需求金錢 ${money}
                            """,
                            'booth': booth
                        }
                        return HttpResponse(msg_template.render(context, request))
                form.save()
                transaction = Transaction.objects.filter(
                    booth=booth,
                    player=player
                ).order_by('-record_time')[0]
                return HttpResponseRedirect(f'/oc/booth/{booth.id}/transactions/{transaction.id}/success')
            else:
                print("INVALID FORM")
        template = loader.get_template('oc/booth_register.html')
        
        # reduce options in the fields
        form.fields['booth'].queryset = Booth.objects.filter(id=booth.id)
        form.fields['player'].queryset = Player.objects.filter(id=user.get_player().id)
        form.fields['marker'].queryset = User.objects.filter(id=request.user.id)
        context = {
            'action_path': f'transaction/{type}',
            'booth': booth,
            'user': user,
            'marker': request.user,
            'scan_type': type,
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

def redirect_to_booth(request):
    return list_booth(request)

def get_contact(request, encrypted_id=""):
    contacts = ContactPerson.objects.all()
    template = loader.get_template('contact.html')
    context = {
        'contacts': contacts,
        'encrypted_id': encrypted_id
    }
    return HttpResponse(template.render(context, request))