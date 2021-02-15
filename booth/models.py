from django.db import models
from account.models import User
# from player.models import Player

# Create your models here.
class BoothRequirement(models.Model):
    def __str__ (self):
        return self.name

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    overall_score = models.IntegerField(default=0)
    # health_score = models.IntegerField(default=0)
    # academic_score = models.IntegerField(default=0)
    # growth_score = models.IntegerField(default=0)
    # relationship_score = models.IntegerField(default=0)
    # joy_score = models.IntegerField(default=0)
    # money = models.IntegerField(default=0)

    def check_player(self, player):
        failed_list = []
        player_scores = player.get_scores()
        for score in ['health_score', 'academic_score', 'growth_score', 'relationship_score', 'joy_score']:
            if player_scores[score] < getattr(self, score):
                failed_list.append(score)
        return failed_list

class BoothScoring(models.Model):
    def __str__(self):
        return self.name

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    overall_score = models.IntegerField(blank=True, null=True)
    # health_score = models.IntegerField(blank=True, null=True)
    # academic_score = models.IntegerField(blank=True, null=True)
    # growth_score = models.IntegerField(blank=True, null=True)
    # relationship_score = models.IntegerField(blank=True, null=True)
    # joy_score = models.IntegerField(blank=True, null=True)
    # money = models.IntegerField(blank=True, null=True)

class Booth(models.Model):
    def __str__(self):
        return self.name

    id = models.CharField(max_length=3, primary_key=True)
    booth_in_charge = models.ForeignKey(
        User, 
        related_name='booth_in_charge', 
        on_delete=models.CASCADE, 
        null=True, blank=True
    )
    booth_admins = models.ManyToManyField(User, related_name='booth_admins')
    score_options = models.ManyToManyField(BoothScoring, related_name='score_options')
    name = models.CharField(max_length=50)
    requirement = models.ForeignKey(BoothRequirement, on_delete=models.CASCADE)

class Participation(models.Model):
    def __str__(self):
        return "{} - {} {}".format(self.booth.name, self.player.user.nick_name, self.player.user.last_name)

    id = models.AutoField(primary_key=True)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    player = models.ForeignKey('player.Player', on_delete=models.CASCADE)
    record_time = models.DateTimeField(auto_now_add=True, blank=True)
    score = models.ForeignKey(BoothScoring, on_delete=models.CASCADE)
    # health_score = models.IntegerField(default=0)
    # academic_score = models.IntegerField(default=0)
    # growth_score = models.IntegerField(default=0)
    # relationship_score = models.IntegerField(default=0)
    # joy_score = models.IntegerField(default=0)
    # money = models.IntegerField(default=0)
    