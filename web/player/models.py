from django.db import models
from booth.models import Participation, Transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
# from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models import Sum, Max, Subquery, Q, F
import pandas as pd

# Create your models here.
LIVE_STATUS_CHOICES = [
    ('active', 'active'),
    ('inactive', 'inactive')
]


class Player(models.Model):
    def __str__(self):
        if self.active:
            return "{} {}{}".format(self.user.get_id(), self.user.last_name, self.user.first_name)
        else:
            return "{} (inactive)".format(self.user.get_id())
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

    def get_scores(self):
        result_dict = {
            'money': self.get_score('money'),
            'health_score': self.get_score('health_score'),
            'skill_score': self.get_score('skill_score'),
            'growth_score': self.get_score('growth_score'),
            'relationship_score': self.get_score('relationship_score'),
            'academic_level': self.get_score('academic_level')
        }
        print(result_dict)
        result_dict['total_score'] = result_dict['health_score'] + \
                                     result_dict['skill_score'] + \
                                     result_dict['growth_score'] + \
                                     result_dict['relationship_score'] 
        return result_dict
        
    def get_score(self, score_name):
        score_list = []
        score_list.append(getattr(self, 'born_' + score_name))
        # participations
        participations = Participation.objects.filter(player=self)
        for parti in participations:
            parti_score = getattr(parti.score, score_name)
            if parti_score:
                print(parti, score_name, parti_score)
                score_list.append(parti_score)
        # transactions
        if score_name == 'money':
            transactions = Transaction.objects.filter(player=self)
            for t in transactions:
                if t.type == 'receive':
                    score_list.append(t.money * -1)
                if t.type == 'pay':
                    score_list.append(t.money)
        if len(score_list) > 0:
            if score_name == 'academic_level': # If Score name is academic level, return maximum academic level
                return max(score_list)
            else:
                print(score_list)
                return sum(score_list)
        else:
            return 0

    @staticmethod
    def get_total_score_list():
        born_df = pd.DataFrame(Player.objects \
            .filter(user__user_type = 'student') \
            .values(uid=F('user__id')) \
            .annotate(
                born_health=Max('born_health_score'),
                born_skill=Max('born_skill_score'),
                born_growth=Max('born_growth_score'),
                born_relationship=Max('born_relationship_score'),
            )
        ).fillna(0)
        participation_df = pd.DataFrame(Participation.objects \
            .filter(player__user__user_type = 'student') \
            .values(uid=F('player__user__id')) \
            .annotate(
                participation_health=Sum('score__health_score'),
                participation_skill=Sum('score__skill_score'),
                participation_growth=Sum('score__growth_score'),
                participation_relationship=Sum('score__relationship_score'),
            )
        ).fillna(0)
        score_df = born_df.copy()
        if len(participation_df) > 0:
            score_df = score_df.merge(participation_df, how='left', on='uid')
        score_df = score_df.set_index('uid').sum(axis=1).reset_index()
        score_df.rename(columns={0: 'total_score'}, inplace=True)
        score_df = score_df.sort_values('total_score', ascending=False)
        return score_df

    @staticmethod
    def get_rich_list():
        born_df = pd.DataFrame(Player.objects \
            .filter(user__user_type = 'student') \
            .values(uid=F('user__id')) \
            .annotate(
                born_money=Max('born_money')
            )
        )
        # born_df.rename(columns={'id': 'player'}, inplace=True)
        participation_df = pd.DataFrame(Participation.objects \
            .filter(player__user__user_type = 'student') \
            .values(uid=F('player__user__id')) \
            .annotate(
                participation_money=Sum('score__money')
            )
        )
        transaction_df = pd.DataFrame(Transaction.objects \
            .filter(player__user__user_type = 'student') \
            .values(uid=F('player__user__id')) \
            .annotate(
                receive=Sum('money', filter=Q(type='receive')),
                pay=Sum('money', filter=Q(type='pay'))
            )
        )
        concat_df = pd.concat([born_df, participation_df, transaction_df])
        concat_df['total_money'] = concat_df['born_money'].fillna(0) 
        if len(participation_df) > 0:
            concat_df['total_money'] += concat_df['participation_money'].fillna(0)
        if len(transaction_df) > 0:
            concat_df['total_money'] +=  concat_df['pay'].fillna(0) - concat_df['receive'].fillna(0)
        money_df = concat_df.groupby('uid', as_index=False)['total_money'].sum()
        money_df['uid'] = money_df['uid'].astype('str')
        return money_df.sort_values('total_money', ascending=False)

class InstructorScore(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    comments = models.TextField(max_length=1000, null=True, blank=True)
    record_time = models.DateTimeField(auto_now_add=True, blank=True)


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