from django.db import models
from booth.models import Participation, Transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
# from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from booth.models import Transaction, Participation
from django.db.models import Sum, Max, Subquery, Q, F
import pandas as pd
import pytz
from datetime import datetime

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
        #  = {
        #     'health_score': participations['health_score'],
        #     'skill_score': participations['skill_score'],
        #     'growth_score': participations['growth_score'],
        #     'relationship_score': participations['relationship_score'],
        #     'money': participations['money'] + transactions['money'],
        #     'deposit': transactions['deposit'],
        #     'academic_level': participations['academic_level'],
        #     'flat': participations['flat'],
        #     ''
        # }

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
        participation_df = pd.DataFrame(Participation.objects \
                                        # .filter(player__user__user_type = 'student') \
                                        .values('player') \
                                        .annotate(money=Sum('score__money')))
        return participation_df.sort_values('money', ascending=False)

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