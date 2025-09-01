from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class UserModel(AbstractUser):
    name = models.CharField(max_length=36, validators=[MinLengthValidator(4)], blank=True, null=True)
    username = models.CharField(max_length=16, validators=[MinLengthValidator(4)], unique=True, blank=False, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(blank=True, max_length=350)
    birth_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.username
