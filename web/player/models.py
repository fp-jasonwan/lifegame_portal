from django.db import models
from booth.models import Participation, Transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce, Least
# from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from booth.models import Transaction, Participation
from django.db.models import Sum, Max, Subquery, Q, F, Avg, Count, Min, Max, Sum, F, Q
from django.db.models import Value, IntegerField, FloatField, When, Case
from django.db.models.functions import Coalesce, Greatest, Floor, Cast
import pandas as pd
import random
# Create your models here.
LIVE_STATUS_CHOICES = [
    ('active', 'active'),
    ('inactive', 'inactive')
]
ACADEMIC_CHOICES = (
    (0, '無學歷'),
    (1, '小學畢業'),
    (2, '中學畢業'),
    (3, '大專畢業'),
    (4, '大學畢業')
)

class Player(models.Model):
    def __str__(self):
        if self.active:
            return "{} - {}{}".format(self.user.id, self.user.last_name, self.user.first_name)
        else:
            return "{} (已死亡)".format(self.user.id)
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
    born_academic_level = models.IntegerField(choices=ACADEMIC_CHOICES)
    born_steps = models.IntegerField()
    born_defect = models.CharField(max_length=100, blank=True, null=True)
    inactive_reason = models.CharField(max_length=200, blank=True, null=True)

    def get_score_summary(self):
        born_status = self.get_born_status()
        participations = self.get_participation_summary()
        transactions = self.get_transaction_summary()
        academic_dict = dict((x, y) for x, y in ACADEMIC_CHOICES)
        df = pd.DataFrame([born_status, participations, transactions]).fillna(0)
        df['academic_level'] = df['academic_level'].astype(int)
        int_cols = ['academic_level', 'flat', 'steps']
        agg_dict = {col: 'max' if col in ['academic_level'] else 'sum' for col in df.columns}
        result_dict = df.agg(agg_dict).astype(int).to_dict()
        # result_dict['academic_level'] = academic_dict[result_dict['academic_level']]
        result_dict['total_score'] = result_dict['health_score'] + \
                                     result_dict['skill_score'] + \
                                     result_dict['growth_score'] + \
                                     result_dict['relationship_score'] 
        return result_dict
    
    def check_eligibility(self, score_dict):
        eligibility = []
        player_scores = self.get_score_summary()
        for score in ['health_score', 'skill_score', 'growth_score', 'relationship_score']:
            if score_dict[score] < 0: # If the score is negative
                if player_scores[score] < abs(score_dict[score]):
                    eligibility.append({
                        'score': score,
                        'player': player_scores[score],
                        'requirement': score_dict[score]
                    })
        if score_dict['money'] < 0: # If the score is negative
            if player_scores['cash'] < abs(score_dict['money']):
                eligibility.append({
                        'score': 'cash',
                        'player': player_scores['cash'],
                        'requirement': score_dict['money']
                    })
        return eligibility

    def get_born_status(self):
        return {
            'health_score': self.born_health_score,
            'skill_score': self.born_skill_score,
            'growth_score': self.born_growth_score,
            'relationship_score': self.born_relationship_score,
            'cash': self.born_money,
            'academic_level': self.born_academic_level,
            'steps': self.born_steps,
        }

    def get_participation_summary(self):
        return self.participation_player.aggregate(
            health_score=Coalesce(Sum('health_score'), Value(0)),
            skill_score=Coalesce(Sum('skill_score'), Value(0)),
            growth_score=Coalesce(Sum('growth_score'), Value(0)),
            relationship_score=Coalesce(Sum('relationship_score'), Value(0)),
            cash=Coalesce(Sum('money'), Value(0)),
            academic_level=Coalesce(Max('academic_level'), Value(0)),
            steps=Coalesce(Sum('steps'), Value(0)),
            flat=Coalesce(Max('flat'), Value(0)),
        )

    def get_transaction_summary(self):
        pay = Case(
            When(type='pay', then='money'), 
            default=Value(0.0),
            output_field = FloatField()
        )
        receive = Case(
            When(type='receive', then='money'), 
            default=Value(0.0),
            output_field = FloatField()
        )
        deposit = Case(
            When(type='deposit', then='money'), 
            default=Value(0.0),
            output_field = FloatField()
        )
        withdrawal = Case(
            When(type='withdrawal', then='money'), 
            default=Value(0.0),
            output_field = FloatField()
        )
        withdrawal_with_interest = Case(
            When(type='withdrawal', then=F('money') * (Value(1.0) + F('interest_rate'))), 
            default=Value(0.0),
            output_field = FloatField()
        )
        return self.transaction_player.aggregate(
            health_score=Sum(Value(0.0)),
            skill_score=Sum(Value(0.0)),
            growth_score=Sum(Value(0.0)),
            relationship_score=Sum(Value(0.0)),
            cash=Sum(pay + withdrawal_with_interest - receive - deposit),
            bank_amount=Sum(deposit-withdrawal),
            academic_level=Sum(Value(0.0)),
            steps=Sum(Value(0.0)),
            pay=Sum(pay),
            receive=Sum(receive),
            deposit=Sum(deposit),
            withdrawal=Sum(withdrawal)
        )


    def get_score(self, score_name):
        return self.get_score_summary()[score_name]

    @staticmethod
    def get_negative_steps_list():
        return Player.objects.filter(Q(user__user_type='student'), Q(active=True)).values('user').annotate(
            steps = Max(F('born_steps')) \
                    + Sum(Coalesce('participation_player__steps', Value(0))) \
        ).filter(steps__lt=0).order_by('-steps')
    
    @staticmethod
    def get_total_score_list(no_of_rows=10):
        return Player.objects.filter(Q(user__user_type='student'), Q(active=True)).values('user').annotate(
            mark = Max(F('born_health_score')) \
                    + Sum(Coalesce('participation_player__health_score', Value(0))) \
                    + Max(F('born_skill_score')) \
                    + Sum(Coalesce('participation_player__skill_score', Value(0))) \
                    + Max(F('born_growth_score')) + Sum(Coalesce('participation_player__growth_score', Value(0))) \
                    + Max(F('born_relationship_score')) \
                    + Sum(Coalesce('participation_player__relationship_score', Value(0)))
        ).order_by('-mark')[:no_of_rows]

    @staticmethod
    def get_rich_list(no_of_rows=10):
        pay = Case(
            When(transaction_player__type='pay', then='transaction_player__money'), 
            default=Value(0.0),
            output_field = FloatField()
        )
        receive = Case(
            When(transaction_player__type='receive', then='transaction_player__money'), 
            default=Value(0.0),
            output_field = FloatField()
        )
        deposit = Case(
            When(transaction_player__type='deposit', then='transaction_player__money'), 
            default=Value(0.0),
            output_field = FloatField()
        )
        withdrawal = Case(
            When(transaction_player__type='withdrawal', then='transaction_player__money'), 
            default=Value(0.0),
            output_field = FloatField()
        )
        withdrawal_with_interest = Case(
            When(transaction_player__type='withdrawal', then=F('transaction_player__money') * (Value(1.0) + F('transaction_player__interest_rate'))), 
            default=Value(0.0),
            output_field = FloatField()
        )
        return Player.objects.filter(Q(user__user_type='student'), Q(active=True)).values('user').annotate(
            mark = Sum(F('born_money') + receive + withdrawal_with_interest - pay - deposit)
        ).order_by('-mark')[:no_of_rows]


def create_player(instance, created, raw, **kwargs):
    # Ignore fixtures and saves for existing courses.
    if not created or raw:
        return
    
    random_index = {
        'money': [10000,10000,15000,20000,25000,30000,35000,40000,45000,50000],
        'health_score': [20, 40, 40, 60, 60, 80, 80, 100, 100, 120],
        'skill_score': [20, 20, 40, 40, 60, 60, 80, 100, 120, 130],
        'growth_score': [5, 5, 5, 10, 10, 15, 20, 25, 30, 35],
        'relationship_score': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'academic_level': [0, 0, 0, 0, 1, 1, 1, 2, 2, 4]
    }
    Player.objects.create(
        user = instance,
        active=True,
        born_money=random.choice(random_index['money']),
        born_health_score=random.choice(random_index['health_score']),
        born_skill_score=random.choice(random_index['skill_score']),
        born_growth_score=random.choice(random_index['growth_score']),
        born_relationship_score=random.choice(random_index['relationship_score']),
        born_academic_level=random.choice(random_index['academic_level']),
        born_steps=15,
        born_defect = ''
    )


models.signals.post_save.connect(create_player, sender="account.User", dispatch_uid='create_player')