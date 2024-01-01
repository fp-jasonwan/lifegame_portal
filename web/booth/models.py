from django.db import models
import datetime
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
        # for score in ['health_score', 'skill_score', 'growth_score', 'relationship_score', 'money']:
        #     print(score, datetime.datetime.now())
        #     if player_scores[score] < getattr(self, score):
        #         failed_list.append(score)
        return failed_list

class BoothScoring(models.Model):
    def __str__(self):
        return self.name

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50)
    health_score = models.IntegerField(blank=True, null=True)
    skill_score = models.IntegerField(blank=True, null=True)
    growth_score = models.IntegerField(blank=True, null=True)
    relationship_score = models.IntegerField(blank=True, null=True)
    money = models.IntegerField(blank=True, null=True)
    academic_level = models.IntegerField(blank=True, null=True)
    steps = models.IntegerField(blank=True, null=True)

class Booth(models.Model):
    def __str__(self):
        
        return f"{self.id[:2]} - {self.name}"

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
        # for score in ['health_score', 'skill_score', 'growth_score', 'relationship_score', 'money']:
        #     if player_scores[score] < getattr(self, score):
        #         failed_list.append(score)
        return failed_list

    id = models.CharField(max_length=10, primary_key=True)
    booth_in_charge = models.ForeignKey(
        'account.User', 
        related_name='booth_in_charge', 
        on_delete=models.CASCADE, 
        null=True, blank=True
    )
    booth_admins = models.ManyToManyField('account.User', related_name='booth_admins', blank=True)
    name = models.CharField(max_length=50)
    score_options = models.ManyToManyField(BoothScoring, related_name='booth_scores', blank=True)
    # requirement = models.ForeignKey(BoothRequirement, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    health_score = models.IntegerField(blank=True, null=True)
    skill_score = models.IntegerField(blank=True, null=True)
    growth_score = models.IntegerField(blank=True, null=True)
    relationship_score = models.IntegerField(blank=True, null=True)
    money = models.IntegerField(blank=True, null=True)
    academic_level = models.IntegerField(blank=True, null=True)
    steps = models.IntegerField(blank=True, null=True)

class Participation(models.Model):
    def __str__(self):
        return "{} - {} at {}".format(self.booth.name, self.player.user.get_id(), self.record_time.strftime("%Y%m%d %H:%M:%S"))

    def get_time(self):
        return self.record_time.strftime("%d/%m %H:%S")
    
    id = models.AutoField(primary_key=True)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    player = models.ForeignKey('player.Player', on_delete=models.CASCADE)
    record_time = models.DateTimeField(auto_now_add=True, blank=True)
    score = models.ForeignKey(BoothScoring, on_delete=models.CASCADE)
    remarks = models.TextField(max_length=1000, null=True, blank=True)
    marker = models.ForeignKey('account.User', on_delete=models.CASCADE)

class Transaction(models.Model):
    def __str__(self):
        if self.type == 'pay':
            return f'{self.booth} paid ${self.money} to {self.player} at {self.record_time}'
        if self.type == 'receive':
            return f'{self.booth} received ${self.money} from {self.player} at {self.record_time}'
        return False

    def get_time(self):
        return self.record_time.strftime("%d/%m %H:%S")
        
    def get_amount(self):
        if self.type == 'pay':
            return self.money
        else:
            return self.money * -1

    id = models.AutoField(primary_key=True)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    player = models.ForeignKey('player.Player', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=(
        ('pay', 'pay'), ('receive', 'receive')
    ))
    record_time = models.DateTimeField(auto_now_add=True, blank=True)
    money = models.IntegerField()
    remarks = models.TextField(max_length=1000, null=True, blank=True)
    marker = models.ForeignKey('account.User', on_delete=models.CASCADE)

class BoothTraffic(models.Model):
    def is_participated(self):
        return Participation.objects.filter(
            player=self.player,
            booth=self.booth
        ).exists()

    # user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    player = models.ForeignKey('player.Player', on_delete=models.CASCADE)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    record_time = models.DateTimeField(auto_now_add=True, blank=True)
