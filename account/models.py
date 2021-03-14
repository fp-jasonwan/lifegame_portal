from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from booth.models import BoothTraffic
# Create your models here.

class User(AbstractUser):
    def __str__(self):
        return "{} - {} {}".format(self.id, self.last_name, self.first_name)

    user_type = models.CharField(
        max_length=10,
        choices=(('student', 'student'), ('oc', 'oc'),('admin', 'admin'), ('instructor', 'instructor')),
        blank=True, null=True
        )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.IntegerField(blank=True, null=True )
    icon = models.ImageField(blank=True, null=True, upload_to='profile/', default='profile/person.png')

    def get_last_seen(self):
        last_seen = BoothTraffic.objects.filter(user=self).order_by('-record_time').first()
        return last_seen