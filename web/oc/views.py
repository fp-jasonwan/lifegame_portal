from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from booth.models import Booth, Participation, BoothScoring, Transaction
from booth.forms import ParticipationForm, BoothSettingsForm, BoothScoringForm, TransactionForm
from account.models import User
from django.contrib import messages
from player.models import Player
from player.views import get_profile
from player.forms import InstructorCommentForm
from .models import ContactPerson
from booth.views import show_participation
from django.db.models import Q
# Create your views here.
# Create your views here.
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
import datetime
import random
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

score_translation = {
        'health_score': '健康',
        'skill_score': '技能',
        'growth_score': '成長',
        'relationship_score': '關係',
        'money': '金錢'
    }

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

@login_required(login_url="/oc")
def search_profile(request, encrypted_id="", booth_id=""):

    # profile = get_object_or_404(Student, user=request.user)
    template = loader.get_template('oc/search_profile.html')
    context = {
    }
    if encrypted_id == "":
        return HttpResponse(template.render(context, request))
    else:
        if encrypted_id.isnumeric():
            user = get_object_or_404(User, id=int(encrypted_id))
            player = user.player
        else:
            user = get_object_or_404(User, encrypted_id=encrypted_id)
            player = user.player
        
        # If the user does not exist, return error
        if user.player is None:
            msg_template = loader.get_template('oc/booth_message.html')
            context['error_type'] = 'unknown_user'
            context['message'] = '此玩家的角色已經死亡,請到靈堂重生!'
            return HttpResponse(msg_template.render(context, request))
        
        scores = player.get_score_summary()
        participations = Participation.objects.filter(player=player).all().order_by('-record_time')
        transactions = Transaction.objects.filter(player=player).all().order_by('-record_time')
        template = loader.get_template('oc/player_profile.html')
        context = {
            'scores': scores,
            'player': player,
            'encryped_id': player.user.id,
            'participations': participations,
            'transactions': transactions
        }
        if booth_id:
            context['booth'] = Booth.objects.get(id=booth_id)
        return HttpResponse(template.render(context, request))
        # return get_profile(request, encrypted_id)
        # return redirect('/oc/booth/{}/register/{}'.format(booth.id, user.id))
    return HttpResponse(template.render(context, request))
    # return HttpResponse("You're voting on question %s." % question_id)


@login_required(login_url="/oc")
def list_booth(request, type=""):
    booths = Booth.objects.filter(booth_admins__in=[request.user]).order_by('id')
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
        return redirect('/oc/booth/' + str(booths[0].id))
    else:
        return redirect('404')

@login_required(login_url="/oc")
def booth_home(request, booth_id):
    booth = get_object_or_404(Booth, id=booth_id)
    request.session['booth'] = booth.id
    template = loader.get_template('oc/booth_home.html')

    if request.method == 'POST':
        booth.is_active = request.POST['is_active'] == 'true'
        booth.save()
    context = {
        'booth': booth
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url="/oc")
def scan_player(request, booth_id):
    booth = get_object_or_404(Booth, id=booth_id)
    template = loader.get_template('oc/check_player.html')
    context = {
        'booth': booth,
        'type': 'check'
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url="/oc")
def check_player(request, booth_id="", encrypted_id=""):
    booth = get_object_or_404(Booth, id=booth_id)
    if encrypted_id.isnumeric():
        user = get_object_or_404(User, id=encrypted_id)
    else:
        user = get_object_or_404(User, encrypted_id=encrypted_id)
    player = user.player
    # If the user does not exist, return error
    if hasattr(user, 'player') == False:
        context['error_type'] = 'unknown_user'
        context['message'] = '此玩家的角色已經死亡,請請到靈堂重生!'
        return HttpResponse(msg_template.render(context, request))
    request.session['booth'] = booth.id
    msg_template = loader.get_template('oc/booth_message.html')
    context = {
        'booth': booth,
        'booth_scores': booth.get_requirements(),
        'player_scores': player.get_score_summary(),
        'score_translation': score_translation,
        'score_types': ['health_score', 'skill_score', 'growth_score', 'relationship_score', 'money']
    }

    
    # Check player eligibility
    # eligibility = booth.check_player(player)
    # if len(eligibility) == 0:
    return redirect('/oc/booth/{}/register/{}'.format(booth.id, user.id)) 
    # else:
    #     context['eligibility'] = eligibility
    #     context['error_type'] = 'not_eligible'
    #     context['message'] = '此玩家不符合攤位要求!'
    #     return HttpResponse(msg_template.render(context, request))

@login_required(login_url="/oc")
def register_page(request, booth_id, encrypted_id):
    booth = get_object_or_404(Booth, id=booth_id)
    score_options = BoothScoring.objects.filter(booth=booth, active=True).all()
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

@login_required(login_url="/oc")
def get_register_score(request, booth_id, user_id):
    booth = get_object_or_404(Booth, id=booth_id)
    user = get_object_or_404(User, id=user_id)
    score_options = booth.booth_scoring.filter(active=True).all()
    context = {
        'booth': booth,
        'user': user,
        'score_options': score_options
    }
    template = loader.get_template('oc/booth_register_score.html')
    return HttpResponse(template.render(context, request))


class BoothParticipationView(LoginRequiredMixin, FormView):
    model = Participation
    form_class = ParticipationForm
    template_name = 'oc/booth_register.html'
    success_url = '/oc/booth'
    # def get_success_url(self):
    #     messages.add_message(self.request, messages.INFO, 'form submission success')
    #     return reverse('/oc/booth', args=(self.kwargs['pk'],))
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    def form_valid(self, form):

        
        data = form.cleaned_data
        eligibility = data['player'].check_eligibility(data)
        if len(eligibility) > 0:
            context = {
                'eligibility': eligibility,
                'error_type': 'not_eligible',
                'message': '此玩家不符合攤位要求!'
            }
            msg_template = loader.get_template('oc/booth_message.html')
            return HttpResponse(msg_template.render(context, self.request))
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booth = Booth.objects.get(id=self.kwargs['booth_id'])
        context['booth'] = booth  # Indicate creation
        return context

    def get_initial(self):
        initial = super().get_initial()
        booth = Booth.objects.get(id=self.kwargs['booth_id'])
        player = User.objects.get(id=self.kwargs['user_id']).player
        if 'score_option' in self.request.GET:
            booth_scoring = BoothScoring.objects.get(id=self.request.GET.get('score_option'))
            initial = {**initial, **booth_scoring.__dict__}
        initial['booth'] = booth
        initial['player'] = player
        initial['marker'] = self.request.user
        initial['record_time'] = datetime.datetime.now()
        return initial
        # return super().get_success_url()
        # return HttpResponseRedirect(f'/oc/booth/{booth.id}/participations/{participation.id}/success')


def show_booth_score(request, booth_id):
    booth = get_object_or_404(Booth, id=booth_id)
    score_options = booth.booth_scoring.filter(active=True).all()
    context = {
        'booth': booth,
        'score_options': score_options
    }
    template = loader.get_template('oc/booth_settings.html')
    return HttpResponse(template.render(context, request))



class BoothScoreFormView(FormView):
    model = BoothScoring
    form_class = BoothScoringForm
    template_name = 'oc/booth_settings_scoring.html'
    success_url = '/oc/booth'


    def form_invalid(self, form):
        return super().form_invalid(form)
    def form_valid(self, form):

        # Check player eligibility
        # eligibility = booth.check_player(player)
        # if len(eligibility) == 0:
        #     return redirect('/oc/booth/{}/register/{}'.format(booth.id, user.id)) 
        # else:
        #     context['eligibility'] = eligibility
        #     context['error_type'] = 'not_eligible'
        #     context['message'] = '此玩家不符合攤位要求!'
        #     return HttpResponse(msg_template.render(context, request))
        form.save()

        return super().form_valid(form)
    
    def get_object(self):
        """Retrieve the object based on the URL parameter, if it exists."""
        obj_id = self.kwargs.get('score_id')  # Assumes 'pk' is in the URL
        return get_object_or_404(BoothScoring, id=obj_id) if obj_id else None
    
    def get_form(self, form_class=None):
        """Modify the form to handle both create and update."""
        form = super().get_form(form_class)
        if self.get_object():
            form.instance = self.get_object()  # Set the instance for update
        return form
    
    def get_initial(self):
        initial = super().get_initial()
        obj = self.get_object()
        if obj:
            # initial = initial | obj.__dict__
            for k, v in obj.__dict__.items():
                initial[k] = v
        if 'booth_id' in self.kwargs:
            booth = Booth.objects.get(id=self.kwargs['booth_id'])
            initial['booth'] = booth
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booth = Booth.objects.get(id=self.kwargs['booth_id'])
        context['booth'] = booth  # Indicate creation
        return context

def update_booth_settings_scoring(request, booth_id, score_id):
    request.session['from'] = request.META.get('HTTP_REFERER', '/')
    booth = get_object_or_404(Booth, id=booth_id)
    booth_scoring = get_object_or_404(BoothScoring, id=score_id)
    # if Booth.objects.filter(booth=booth).exists():
    instance = booth_scoring
    form = BoothScoringForm(request.POST or None, instance=instance)
    
    if request.method == 'POST':
        if form.is_valid():
            new_booth_score = BoothScoring(**form.cleaned_data)
            new_booth_score.save()
            
            # original score inactive
            old_score = form.save(commit=False)
            old_score.active = False
            old_score.save()
            msg_template = loader.get_template('oc/booth_message.html')
            context = {
                'booth': booth,
                'message': '成功更新攤位要求!'
            }
            return HttpResponse(msg_template.render(context, request))
    template = loader.get_template('oc/booth_settings_scoring.html')
    
    context = {
        'booth': booth,
        'booth_scoring': booth_scoring,
        'form': form
    }
    return HttpResponse(template.render(context, request))

def create_booth_settings_scoring(request, booth_id):
    request.session['from'] = request.META.get('HTTP_REFERER', '/')
    booth = get_object_or_404(Booth, id=booth_id)
    form = BoothScoringForm(request.POST or None,
        initial = {'booth': booth}
    )
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            msg_template = loader.get_template('oc/booth_message.html')
            context = {
                'booth': booth,
                'message': '成功更新攤位要求!'
            }
            return HttpResponse(msg_template.render(context, request))

    template = loader.get_template('oc/booth_settings_scoring_create.html')
    
    context = {
        'booth': booth,
        'form': form
    }
    return HttpResponse(template.render(context, request))

def update_booth_settings_requirement(request, booth_id):
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
    template = loader.get_template('oc/booth_settings_requirement.html')
    
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
                'message': '此玩家的角色已經死亡,請到靈堂重生!'
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
                if type in ('receive', 'deposit'):
                    player_money = player.get_score('cash')
                    if money > player_money:
                        msg_template = loader.get_template('oc/booth_message.html')
                        context = {
                            'error_type': 'insufficient_amount',
                            'message': f"""
                                玩家金錢不足! 玩家現有現金為${player_money} 
                            """,
                            'booth': booth
                        }
                        return HttpResponse(msg_template.render(context, request))
                if type in ('withdrawal'): 
                    player_deposit = player.get_score('deposit')
                    if money > player_deposit:
                        msg_template = loader.get_template('oc/booth_message.html')
                        context = {
                            'error_type': 'insufficient_amount',
                            'message': f"""
                                玩家銀行存款不足! 玩家現有銀行存款為${player_deposit} 
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
        template = loader.get_template('oc/booth_register_transaction.html')
        
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


# def get_instructor_players(request):
#     instructor = request.user
#     players = Player.objects.all()
#     for p in players:
#         p.__dict__['comment_added'] = InstructorScore.objects.filter(player=p).count() > 0
#     template = loader.get_template('oc/instructor.html')
#     last_seen = Participation.objects.filter()
#     context = {
#         'players': players,
#     }
#     return HttpResponse(template.render(context, request))

# def register_instructor_comment(request, player_id):
#     player = get_object_or_404(Player, id=player_id)
#     try:
#         comment_record = InstructorScore.objects.get(player=player)
#     except:
#         comment_record = None
#     if request.method == 'POST':
#         print(request.POST)
#         form = InstructorCommentForm(request.POST)
#         if form.is_valid():
#             print("VALID FORM")
#             comments = form.cleaned_data['comments']
#             score = form.cleaned_data['score']

#             if not comment_record:
#                 comment_record = InstructorScore(
#                     player = player, 
#                     score=score, 
#                     comments=comments,
#                     instructor=request.user, 
#                 )
#             comment_record.save()
#             messages.success(request, '評分已被記錄!')
#         else:
#             print("INVALID FORM")
#     template = loader.get_template('oc/instructor_comment.html')
    
#     context = {
#         'player': player,
#         'comment': comment_record
#     }
#     return HttpResponse(template.render(context, request))

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

def kill_player(request, booth_id, encrypted_id=None):
    booth = get_object_or_404(Booth, id=booth_id)
    template = loader.get_template('oc/check_player.html')
    msg_template = loader.get_template('oc/booth_message.html')
    context = {
        'booth': booth,
        'scan_type': 'kill'
    }
    # If the user does not exist, return error
    if encrypted_id:
        if encrypted_id.isnumeric():
            user = get_object_or_404(User, id=encrypted_id)
        else:
            user = get_object_or_404(User, encrypted_id=encrypted_id)
        if user.player is None:
            context['error_type'] = 'unknown_user'
            context['message'] = 'error'
            return HttpResponse(msg_template.render(context, request))
        
        player = user.get_player()
        player.active = False
        player.save()
        context['message'] = '此玩家的角色已被死神殺害,請重新領取身份!'
        return HttpResponse(msg_template.render(context, request))
    return HttpResponse(template.render(context, request))

def check_player(request, booth_id="", encrypted_id=""):
    booth = get_object_or_404(Booth, id=booth_id)
    msg_template = loader.get_template('oc/booth_message.html')
    if encrypted_id.isnumeric():
        user = get_object_or_404(User, id=encrypted_id)
    else:
        user = get_object_or_404(User, encrypted_id=encrypted_id)
    
    context = {
        'booth': booth,
        'booth_scores': booth.get_requirements(),
        'score_translation': score_translation,
        'score_types': ['health_score', 'skill_score', 'growth_score', 'relationship_score', 'money']
    }
    # If the user does not exist, return error
    if user.player is None:
        context['error_type'] = 'unknown_user'
        context['message'] = '此玩家的角色已經死亡,請到靈堂重生!'
        return HttpResponse(msg_template.render(context, request))
    
    player = user.player
    request.session['booth'] = booth.id
    context['player_scores'] = player.get_score_summary()

    # Check player eligibility
    # eligibility = booth.check_player(player)
    # if len(eligibility) == 0:
    return redirect('/oc/booth/{}/register/{}/option'.format(booth.id, user.id)) 
    # else:
    #     context['eligibility'] = eligibility
    #     context['error_type'] = 'not_eligible'
    #     context['message'] = '此玩家不符合攤位要求!'
    #     return HttpResponse(msg_template.render(context, request))

def create_player(request, booth_id, encrypted_id=None):
    booth = get_object_or_404(Booth, id=booth_id)
    template = loader.get_template('oc/check_player.html')
    msg_template = loader.get_template('oc/booth_message.html')
    context = {
        'booth': booth,
        'scan_type': 'create'
    }
    # If the user does not exist, return error
    if encrypted_id:
        if encrypted_id.isnumeric():
            user = get_object_or_404(User, id=encrypted_id)
        else:
            user = get_object_or_404(User, encrypted_id=encrypted_id)
        random_index = {
            'money': [10000,10000,15000,20000,25000,30000,35000,40000,45000,50000],
            'health_score': [20, 40, 40, 60, 60, 80, 80, 100, 100, 120],
            'skill_score': [20, 20, 40, 40, 60, 60, 80, 100, 120, 130],
            'growth_score': [5, 5, 5, 10, 10, 15, 20, 25, 30, 35],
            'relationship_score': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            'academic_level': [0, 0, 0, 0, 1, 1, 1, 2, 2, 4]
        }
        player = Player.objects.create(
            user=user,
            born_money=random.choice(random_index['money']),
            born_health_score=random.choice(random_index['health_score']),
            born_skill_score=random.choice(random_index['skill_score']),
            born_growth_score=random.choice(random_index['growth_score']),
            born_relationship_score=random.choice(random_index['relationship_score']),
            born_academic_level=random.choice(random_index['academic_level']),
            born_steps=15,
            born_defect=''
        )
        return redirect(f"/oc/search_profile/{user.id}")
    return HttpResponse(template.render(context, request))


def get_negative_steps_list(request, booth_id):
    booth = get_object_or_404(Booth, id=booth_id)
    template = loader.get_template('oc/negative_steps.html')
    score_list = Player.get_negative_steps_list()
    context = {
        'booth': booth,
        'list_name': '逃稅玩家',
        'mark_name': '步數',
        'description': '以上玩家現時的步數為負數',
        'list': score_list,
        'now': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return HttpResponse(template.render(context, request))
