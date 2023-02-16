from django.db import models
from booth.models import Participation
from django.db.models import Sum
from django.db.models.functions import Coalesce
# from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
LIVE_STATUS_CHOICES = [
    ('active', 'active'),
    ('inactive', 'inactive')
]

class BornStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    health_score = models.IntegerField()
    skill_score = models.IntegerField()
    growth_score = models.IntegerField()
    relationship_score = models.IntegerField()
    money = models.IntegerField()
    academic_level = models.IntegerField()
    steps = models.IntegerField()
    
class Education(models.Model):
    id = models.AutoField(primary_key=True)
    level = models.IntegerField()
    name = models.CharField(max_length=50)

class Player(models.Model):
    def __str__(self):
        return "{} - {} {}".format(self.user.id, self.user.first_name, self.user.last_name)
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField('account.User', on_delete=models.CASCADE, null=True, blank=True)
    born_status = models.ForeignKey(BornStatus, on_delete=models.CASCADE, null=True, blank=True)
    born_education_level = models.ForeignKey(Education, on_delete=models.CASCADE, null=True, blank=True)
    live_status = models.CharField(
        choices=LIVE_STATUS_CHOICES,
        default='active',
        max_length=8
    )

    def get_scores(self):
        result_dict = {
            'money': self.get_score('money'),
            'health_score': self.get_score('health_score'),
            'skill_score': self.get_score('skill_score'),
            'growth_score': self.get_score('growth_score'),
            'relationship_score': self.get_score('relationship_score'),
            'joy_score': self.get_score('joy_score'),
            'academic_level': self.get_score('academic_level')
        }
        print(result_dict)
        result_dict['total_score'] = result_dict['health_score'] + \
                                     result_dict['skill_score'] + \
                                     result_dict['growth_score'] + \
                                     result_dict['relationship_score'] 
        return result_dict
        
    def get_score(self, score_name):
        # If Score name does not exist
        if score_name not in self.born_status.__dict__:
            return False

        score_list = []
        score_list.append(getattr(self.born_status, score_name))
        participations = Participation.objects.filter(player=self)
        for parti in participations:
            parti_score = getattr(parti.score, score_name)
            if parti_score:
                score_list.append(parti_score)
        if len(score_list) > 0:
            if score_name == 'academic_level': # If Score name is academic level, return maximum academic level
                return max(score_list)
            else:
                return sum(score_list)
        else:
            return 0

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
        born_status=BornStatus.objects.get(id=1),
        born_education_level=Education.objects.get(id=1),
        live_status='active'
    )


models.signals.post_save.connect(create_player, sender="account.User", dispatch_uid='create_player')