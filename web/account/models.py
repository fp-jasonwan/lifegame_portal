from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from booth.models import Booth
from player.models import Player
from django.http import Http404
from django.utils.crypto import get_random_string
# Create your models here.
from django.contrib import messages

def generate_encrypted_string():
    return get_random_string(32)

class User(AbstractUser):
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.id} - {self.last_name}{self.first_name}".format('{:03d}'.format(self.id), self.last_name, self.first_name)

    def is_oc(self):
        return self.user_type in ('oc', 'admin')

    def get_player(self):
        return Player.objects.filter(user=self, active=True).first()

    @property
    def best_booth(self):
        return BoothVoting.objects.get(user=self)
    
    @property
    def player(self):
        try:
            return Player.objects.get(
                user=self,
                active=True
            )
        except :
            raise Http404("此玩家的角色已經死亡,請到靈堂重生!")

    user_type = models.CharField(
        max_length=10,
        choices=(('student', 'student'), ('oc', 'oc'),('admin', 'admin'), ('instructor', 'instructor'),
                 ('vip', 'vip')),
        blank=True, null=True
        )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.IntegerField(blank=True, null=True )
    school = models.CharField(max_length=100, blank=True, null=True)
    encrypted_id = models.CharField(max_length=32, default=generate_encrypted_string)
    school_code = models.CharField(max_length=2, blank=True, null=True)
    instructor_group = models.ForeignKey(
        'account.InstructorGroup', 
        on_delete=models.CASCADE,
        related_name='instructor_group_student',
        null=True,
        blank=True
    )
    
class InstructorGroup(models.Model):
    def get_player(self):
        players = Player.objects.filter(user__in=self.instructor_group_student.all()).order_by('-active','user__id')
        return players
    
    def __str__(self):
        return self.name
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    instructor = models.ManyToManyField('account.User', related_name='instructor')


class BoothVoting(models.Model):
    class Meta:
        unique_together = ('user', 'booth',)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    booth = models.ForeignKey('booth.Booth', on_delete=models.CASCADE)