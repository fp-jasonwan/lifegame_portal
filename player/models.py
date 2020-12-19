from django.db import models
from booth.models import Participation
from django.db.models import Sum
from account.models import User
# Create your models here.
LIVE_STATUS_CHOICES = [
    ('active', 'active'),
    ('inactive', 'inactive')
]

class BornStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    health_score = models.IntegerField()
    academic_score = models.IntegerField()
    growth_score = models.IntegerField()
    relationship_score = models.IntegerField()
    joy_score = models.IntegerField()
    money = models.IntegerField()
    
class Education(models.Model):
    id = models.AutoField(primary_key=True)
    level = models.IntegerField()
    name = models.CharField(max_length=50)

class Player(models.Model):
    def __str__(self):
        return "{} - {} {}".format(self.user.id, self.user.nick_name, self.user.last_name)
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    born_status = models.ForeignKey(BornStatus, on_delete=models.CASCADE)
    born_education_level = models.ForeignKey(Education, on_delete=models.CASCADE)
    live_status = models.CharField(
        choices=LIVE_STATUS_CHOICES, 
        default='active', 
        max_length=8
    )
    past_user = models.ForeignKey(
        User, 
        related_name='past_user', 
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    
    def get_scores(self):
        return {
            'money': self.get_money(),
            'health': self.get_health_score(),
            'academic': self.get_academic_score(),
            'growth': self.get_growth_score(),
            'relationship': self.get_relationship_score(),
            'joy': self.get_joy_score()
        }

    def get_money(self):
        money = self.born_status.money
        participations = Participation.objects.filter(player=self).aggregate(money=Sum('money'))
        money += participations['money']
        return money
        
    def get_health_score(self):
        health_score = self.born_status.health_score
        participations = Participation.objects.filter(player=self).aggregate(health_score=Sum('health_score'))
        health_score += participations['health_score']
        return health_score
        
    def get_academic_score(self):
        academic_score = self.born_status.academic_score
        participations = Participation.objects.filter(player=self).aggregate(academic_score=Sum('academic_score'))
        academic_score += participations['academic_score']
        return academic_score
        
    def get_growth_score(self):
        growth_score = self.born_status.growth_score
        participations = Participation.objects.filter(player=self).aggregate(growth_score=Sum('growth_score'))
        growth_score += participations['growth_score']
        return growth_score
        
    def get_relationship_score(self):
        relationship_score = self.born_status.relationship_score
        participations = Participation.objects.filter(player=self).aggregate(relationship_score=Sum('relationship_score'))
        relationship_score += participations['relationship_score']
        return relationship_score

    def get_joy_score(self):
        joy_score = self.born_status.joy_score
        participations = Participation.objects.filter(player=self).aggregate(joy_score=Sum('joy_score'))
        joy_score += participations['joy_score']
        return joy_score
