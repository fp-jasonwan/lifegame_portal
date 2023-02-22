from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from booth.models import BoothTraffic, Booth
from player.models import Player
from django.utils.crypto import get_random_string
# Create your models here.

class User(AbstractUser):

    def __str__(self):
        return "{} - {} {}".format(self.id, self.last_name, self.first_name)

    def is_oc(self):
        return self.user_type in ('oc', 'admin')

    def is_player(self):
        return Player.objects.filter(user=self).exists()

    def get_player(self):
        return Player.objects.filter(user=self, active=True).first()

    @property
    def player(self):
        return Player.objects.filter(
            user=self,
            active=True
        ).first()

    user_type = models.CharField(
        max_length=10,
        choices=(('student', 'student'), ('oc', 'oc'),('admin', 'admin'), ('instructor', 'instructor')),
        blank=True, null=True
        )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.IntegerField(blank=True, null=True )
    school = models.CharField(max_length=100, blank=True, null=True)
    encrypted_id = models.CharField(max_length=32, default=get_random_string(length=32))
    
class InstructorGroup(models.Model):
    def get_player(self):
        players = Player.objects.filter(user__in=self.students.all()).order_by('-active')
        return players

    instructor = models.ForeignKey(
        'account.User', 
        on_delete=models.CASCADE,
        related_name='instructor'
    )
    students = models.ManyToManyField('account.User')