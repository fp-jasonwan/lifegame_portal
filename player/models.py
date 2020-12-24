from django.db import models
from booth.models import Participation
from django.db.models import Sum
from django.db.models.functions import Coalesce
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
            'money': self.get_score('money'),
            'health_score': self.get_score('health_score'),
            'academic_score': self.get_score('academic_score'),
            'growth_score': self.get_score('growth_score'),
            'relationship_score': self.get_score('relationship_score'),
            'joy_score': self.get_score('joy_score')
        }
        
    def get_score(self, score_name):
        if score_name not in self.born_status.__dict__:
            return False
        score = getattr(self.born_status, score_name)
        parti_score = Participation.objects.filter(player=self).aggregate(score=Coalesce(Sum(score_name), 0))
        if parti_score['score'] > 0:
            score += parti_score['score']
        return score
