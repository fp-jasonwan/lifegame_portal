from django.db import models
from account.models import User
# from player.models import Player

# Create your models here.
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
    booth_admins = models.ManyToManyField(User, related_name='booth_admins', null=True, blank=True)
    name = models.CharField(max_length=50)

class Participation(models.Model):
    def __str__(self):
        return "{} - {} {}".format(self.booth.name, self.player.user.nick_name, self.player.user.last_name)

    id = models.AutoField(primary_key=True)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    player = models.ForeignKey('player.Player', on_delete=models.CASCADE)
    health_score = models.IntegerField()
    academic_score = models.IntegerField()
    growth_score = models.IntegerField()
    relationship_score = models.IntegerField()
    joy_score = models.IntegerField()
    money = models.IntegerField()
    
class BoothScoring(models.Model):
    def __str__(self):
        return self.name

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    health_score = models.IntegerField(blank=True, null=True)
    academic_score = models.IntegerField(blank=True, null=True)
    growth_score = models.IntegerField(blank=True, null=True)
    relationship_score = models.IntegerField(blank=True, null=True)
    joy_score = models.IntegerField(blank=True, null=True)
    money = models.IntegerField(blank=True, null=True)
