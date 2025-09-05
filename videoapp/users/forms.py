from django import forms
from .models import UserModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("username", "email", "name", "password1", "password2", "bio", "profile_picture", "birth_date")
        
        
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Kullanıcı Adı"),
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label=_("Şifre"),
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )