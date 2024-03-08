from django.db import models
from booth.models import Participation, Transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce, Least
# from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from booth.models import Transaction, Participation
from django.db.models import Sum, Max, Subquery, Q, F, Avg, Count, Min, Max, Sum, F, Q
from django.db.models import Value, IntegerField
from django.db.models.functions import Coalesce, Greatest, Floor
import pandas as pd
import pytz
from datetime import datetime
import numpy as np
# Create your models here.
LIVE_STATUS_CHOICES = [
    ('active', 'active'),
    ('inactive', 'inactive')
]


class Player(models.Model):
    def __str__(self):
        if self.active:
            return "{} {} {}".format(self.user.get_id(), self.user.last_name, self.user.first_name)
        else:
            return "{} (已死亡)".format(self.user.get_id())
            # return "{}{} (inactive)".format(self.user.last_name, self.user.first_name)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            # This code only happens if the objects is
            # not in the database yet. Otherwise it would
            # have pk
            user = self.user
            Player.objects.filter(user=user).update(active=False)
        super(Player, self).save(*args, **kwargs)

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=True)
    born_health_score = models.IntegerField()
    born_skill_score = models.IntegerField()
    born_growth_score = models.IntegerField()
    born_relationship_score = models.IntegerField()
    born_money = models.IntegerField()
    born_academic_level = models.IntegerField()
    born_steps = models.IntegerField()
    born_defect = models.CharField(max_length=100, blank=True, null=True)
    inactive_reason = models.CharField(max_length=200, blank=True, null=True)
    def get_born_scores(self):
        return {
            'health_score': self.born_health_score,
            'skill_score': self.born_skill_score,
            'growth_score': self.born_growth_score,
            'relationship_score': self.born_relationship_score,
            'money': self.born_money,
            'academic_level': self.born_academic_level,
            'steps': self.born_steps,
        }

    def get_scores(self):
        participations = Participation.get_player_participation(self)
        transactions = Transaction.get_player_transactions(self)
        result_dict = participations
        result_dict['money'] += transactions['money']
        result_dict['deposit'] = transactions['deposit']

        # academic level text
        if participations['academic_level']==1: 
            result_dict['academic_level_text'] = '小學畢業'
        elif participations['academic_level']==2: 
            result_dict['academic_level_text'] = '中學畢業'
        elif participations['academic_level']==3: 
            result_dict['academic_level_text'] = '大專畢業'
        elif participations['academic_level']==4: 
            result_dict['academic_level_text'] = '大學畢業'
        else:
            result_dict['academic_level_text'] = ''

        result_dict['total_score'] = result_dict['health_score'] + \
                                     result_dict['skill_score'] + \
                                     result_dict['growth_score'] + \
                                     result_dict['relationship_score'] 
        return result_dict
        
    def get_score(self, score_name):
        return self.get_scores()[score_name]

    @staticmethod
    def get_total_score_list(no_of_rows=10):
        player_df =  pd.DataFrame(
            Player.objects \
                  .filter(user__user_type='student') \
                  .values(
                        player=F('user__id'), 
                        total_score=F('born_health_score') +
                                    F('born_skill_score') +
                                    F('born_relationship_score') +
                                    F('born_growth_score')
            ).all()
        )
        parti_df  = pd.DataFrame(
            Participation.objects \
                         .filter(player__user__user_type='student') \
                         .values('player') \
                         .annotate(total_score=
                            Sum('score__health_score') +
                            Sum('score__skill_score') +
                            Sum('score__relationship_score') +
                            Sum('score__growth_score')
                         )
        )
        best_score_df = pd.concat([parti_df, player_df]).groupby('player', as_index=False)['total_score'].sum()
        
        best_score_df = best_score_df.sort_values('total_score', ascending=False)
        return best_score_df[:no_of_rows]

    @staticmethod
    def get_rich_list(no_of_rows=10):
        parti_money_df = pd.DataFrame(
            Participation.objects \
                         .filter(player__user__user_type='student') \
                         .values(p=F('player__user__id')).annotate(money=Sum('score__money'))
        )
        player_df =  pd.DataFrame(
            Player.objects \
                  .filter(user__user_type='student') \
                  .values(p=F('user__id'), money=F('born_money')).all()
        )
        pay = Coalesce(Sum('money', filter=Q(type='pay')), Value(0))
        receive = Coalesce(Sum('money', filter=Q(type='receive')), Value(0)) 
        deposit = Coalesce(Sum('money', filter=Q(type='deposit')), Value(0))
        withdrawal_money = Coalesce(
            Floor(
                Sum(F('money') * (1 + F('interest_rate')), output_field=IntegerField(), filter=Q(type='withdrawal'))
            ), 
            Value(0)
        )
        withdrawal_deposit = Coalesce(Sum(F('money'), filter=Q(type='withdrawal')), Value(0))
        trx_df = pd.DataFrame(
            Transaction.objects \
                      .filter(player__user__user_type='student') \
                      .values(p=F('player__user__id')) \
                      .annotate(money = pay - receive - deposit + withdrawal_money + deposit - withdrawal_deposit)
        )
        rich_df = pd.concat([parti_money_df, player_df, trx_df]).groupby('p', as_index=False)['money'].sum()
        rich_df = rich_df.rename(columns={'p': 'player'})
        rich_df = rich_df.sort_values('money', ascending=False)
        rich_df['player'] = rich_df['player'].astype('int')
        rich_df['money'] = rich_df['money'].astype('int')
        return rich_df[:no_of_rows]

class InstructorScore(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    comments = models.TextField(max_length=1000, null=True, blank=True)
    record_time = models.DateTimeField(default=datetime.now(pytz.timezone('Asia/Hong_Kong')), blank=True)


def create_player(instance, created, raw, **kwargs):
    # Ignore fixtures and saves for existing courses.
    if not created or raw:
        return

    Player.objects.create(
        user = instance,
        active=True,
        born_health_score = 0,
        born_skill_score = 0,
        born_growth_score = 0,
        born_relationship_score = 0,
        born_money = 0,
        born_academic_level = 0,
        born_steps = 0,
        born_defect = ''
    )


models.signals.post_save.connect(create_player, sender="account.User", dispatch_uid='create_player')