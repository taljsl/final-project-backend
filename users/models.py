from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique = True)
    nickname = models.CharField(max_length=20, blank = True, null= True)
    name = models.CharField(max_length=100, blank=True, null=True)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'