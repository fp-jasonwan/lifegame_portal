from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    def __str__(self):
        return "{} - {} {}".format(self.id, self.nick_name, self.last_name)

    user_type = models.CharField(
        max_length=10,
        choices=(('student', 'student'), ('oc', 'oc'),('admin', 'admin')),
        blank=True, null=True
        )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100, blank=True, null=True)
    icon = models.ImageField(blank=True, null=True, upload_to='profile/')
