from django.db import models
import datetime
from django.db.models import Avg, Count, Min, Max, Sum, F, Q
from django.db.models import Value, IntegerField
from django.db.models.functions import Coalesce, Greatest, Floor
from datetime import datetime
import pytz

# from player.models import Player

# Create your models here.
class BoothRequirement(models.Model):
    def __str__ (self):
        return self.name

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=100)
    health_score = models.IntegerField(default=0)
    skill_score = models.IntegerField(default=0)
    growth_score = models.IntegerField(default=0)
    relationship_score = models.IntegerField(default=0)
    money = models.IntegerField(default=0)

    def check_player(self, player):
        failed_list = []
        player_scores = player.get_scores()
        for score in ['health_score', 'skill_score', 'growth_score', 'relationship_score', 'money', 'academic_level']:
            if player_scores[score] < getattr(self, score):
                failed_list.append(score)
        return failed_list


class Booth(models.Model):
    def __str__(self):
        return f"{self.id[:2]} {self.name}"

    def get_requirements(self):
        result_dict = {
            'health_score': self.health_score,
            'skill_score': self.skill_score,
            'growth_score': self.growth_score,
            'relationship_score': self.relationship_score,
            'money': self.money
        }
        return result_dict

    def check_player(self, player):
        failed_list = []
        player_scores = player.get_scores()
        for score in ['health_score', 'skill_score', 'growth_score', 'relationship_score', 'money']:
            print(score)
            if getattr(self, score, 0):
                if player_scores[score] < getattr(self, score, 0):
                    failed_list.append(score)
        return failed_list

    id = models.CharField(max_length=20, primary_key=True)
    booth_in_charge = models.ForeignKey(
        'account.User', 
        related_name='booth_in_charge', 
        on_delete=models.CASCADE, 
        null=True, blank=True
    )
    booth_admins = models.ManyToManyField('account.User', related_name='booth_admins', blank=True)
    name = models.CharField(max_length=50, verbose_name='攤位名稱')
    # score_options = models.ManyToManyField(BoothScoring, related_name='booth_scores', blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    health_score = models.IntegerField(blank=True, null=True, verbose_name='健康分數')
    skill_score = models.IntegerField(blank=True, null=True, verbose_name='技能分數')
    growth_score = models.IntegerField(blank=True, null=True, verbose_name='成長分數')
    relationship_score = models.IntegerField(blank=True, null=True, verbose_name='關係分數')
    money = models.IntegerField(blank=True, null=True, verbose_name='金錢')
    academic_level = models.IntegerField(blank=True, null=True, verbose_name='學歷')
    steps = models.IntegerField(blank=True, null=True)


class BoothScoring(models.Model):
    def __str__(self):
        return self.name

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='分數名稱')
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, verbose_name="攤位")
    health_score = models.IntegerField(blank=True, null=True, default=0, verbose_name='健康分數')
    skill_score = models.IntegerField(blank=True, null=True, default=0, verbose_name='技能分數')
    growth_score = models.IntegerField(blank=True, null=True, default=0, verbose_name='成長分數')
    relationship_score = models.IntegerField(blank=True, null=True, default=0, verbose_name='關係分數')
    money = models.IntegerField(blank=True, null=True, default=0, verbose_name='金錢')
    academic_level = models.IntegerField(blank=True, null=True, default=0, verbose_name='學歷')
    steps = models.IntegerField(blank=True, null=True, default=0, verbose_name='步數')
    flat = models.IntegerField(blank=True, null=True, default=0, verbose_name='樓宇')
    record_time = models.DateTimeField(default=datetime.now(pytz.timezone('Asia/Hong_Kong')), blank=True, verbose_name="時間")
    active = models.BooleanField(default=True)


class Participation(models.Model):
    def __str__(self):
        return "{} - {} at {}".format(self.booth.name, self.player.user.get_id(), self.record_time.strftime("%Y%m%d %H:%M:%S"))

    def get_time(self):
        return self.record_time.strftime("%d/%m %H:%S")
    
    @staticmethod
    def get_player_participation(player):
        player_participations = Participation.objects.filter(player=player)
        participation_scores = player_participations.aggregate(
            health_score = Coalesce(Sum(F('score__health_score')),0),
            skill_score = Coalesce(Sum(F('score__skill_score')),0),
            growth_score = Coalesce(Sum(F('score__growth_score')),0),
            relationship_score = Coalesce(Sum(F('score__relationship_score')),0),
            money = Coalesce(Sum(F('score__relationship_score')),0),
            academic_level = Coalesce(Max(F('score__academic_level')),1),
            steps = Coalesce(Sum(F('score__steps')),0),
            flat = Coalesce(Sum(F('score__flat')),0),
        )
        return {
            'health_score': participation_scores['health_score'] + player.born_health_score,
            'skill_score': participation_scores['skill_score'] + player.born_skill_score,
            'growth_score': participation_scores['growth_score'] + player.born_growth_score,
            'relationship_score': participation_scores['relationship_score'] + player.born_relationship_score,
            'money': participation_scores['money'] + player.born_money,
            'academic_level': max(participation_scores['academic_level'], player.born_academic_level),
            'steps': participation_scores['steps'] + player.born_steps,
            'flat': participation_scores['flat'] ,
        }

    def get_score(self):
        return {
            'health_score': self.score.health_score,
            'skill_score': self.score.skill_score,
            'growth_score': self.score.growth_score,
            'relationship_score': self.score.relationship_score,
            'money': self.score.money,
            'academic_level': self.score.academic_level,
            'steps': self.score.steps,
            'flat': self.score.flat,
        }

    id = models.AutoField(primary_key=True)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, verbose_name="攤位")
    player = models.ForeignKey('player.Player', on_delete=models.CASCADE, verbose_name="玩家")
    record_time = models.DateTimeField(default=datetime.now(pytz.timezone('Asia/Hong_Kong')), blank=True, verbose_name="時間")
    score = models.ForeignKey(BoothScoring, on_delete=models.CASCADE, verbose_name="分數")
    marker = models.ForeignKey('account.User', on_delete=models.CASCADE, verbose_name="評分員")

class Transaction(models.Model):
    def __str__(self):
        if self.type == 'pay':
            return f'付款${self.money}予玩家{self.player.user.id}'
        if self.type == 'receive':
            return f'從玩家{self.player.user.id}收取${self.money}'
        if self.type == 'deposit':
            return f'玩家{self.player.user.id}存款${self.money}'
        if self.type == 'withdrawal':
            return f'玩家{self.player.user.id}提款${self.money}'
        return False

    def get_time(self):
        return self.record_time.strftime("%d/%m %H:%S")
        
    def get_player_str(self):
        if self.type == 'pay':
            return f'收取${self.money}'
        if self.type == 'receive':
            return f'付款${self.player.user.id}'
        if self.type == 'deposit':
            return f'存款${self.money}'
        if self.type == 'withdrawal':
            return f'提款${self.money}'
        return False
    
    @staticmethod
    def get_player_transactions(player):
        player_trx = Transaction.objects.filter(player=player)
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
        return player_trx.aggregate(
            money = pay - receive - deposit + withdrawal_money,
            deposit = deposit - withdrawal_deposit,
        )

    def get_money(self):
        if self.type == 'pay':
            return self.money
        elif self.type == 'receive':
            return self.money * -1
        elif self.type == 'withdrawal':
            return self.money * (1 + self.interest_rate)
        elif self.type == 'deposit':
            return self.money * -1
        else:
            return 0
    
    def get_deposit(self):
        if self.type == 'withdrawal':
            return self.money * -1
        elif self.type == 'deposit':
            return self.money 
        else:
            return 0

    id = models.AutoField(primary_key=True)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, verbose_name="攤位")
    player = models.ForeignKey('player.Player', on_delete=models.CASCADE, verbose_name="玩家")
    type = models.CharField(
        max_length=10, 
        choices=(
            ('pay', '付款'), 
            ('receive', '收款'),
            ('deposit', '存款'),
            ('withdrawal', '提款'),
        )
        , verbose_name="交易類型"
    )
    record_time = models.DateTimeField(
        default=datetime.now(pytz.timezone('Asia/Hong_Kong')), 
        blank=True, 
        verbose_name="時間"
    )
    money = models.IntegerField(verbose_name="金錢", default=0)
    interest_rate = models.FloatField(verbose_name='利率', default=0, blank=True)
    marker = models.ForeignKey('account.User', on_delete=models.CASCADE, verbose_name="評分員")


class BoothTraffic(models.Model):
    def is_participated(self):
        return Participation.objects.filter(
            player=self.player,
            booth=self.booth
        ).exists()

    # user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    player = models.ForeignKey('player.Player', on_delete=models.CASCADE)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    record_time = models.DateTimeField(default=datetime.now(pytz.timezone('Asia/Hong_Kong')), blank=True)
