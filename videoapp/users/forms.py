from django import forms
from .models import UserModel
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("username", "email", "name", "password1", "password2", "bio", "profile_picture", "birth_date")