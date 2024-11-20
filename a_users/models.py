from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    about = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    password=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
