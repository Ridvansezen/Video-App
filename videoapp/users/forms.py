from django import forms
from .models import UserModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from datetime import date
from django.core.validators import MaxValueValidator



class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(
            years=range(1900, date.today().year + 1),
            attrs={'class': 'form-control'}
        ),
        validators=[MaxValueValidator(limit_value=date.today(), message="Gelecek tarih seçilemez!")]
    )
    
    
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
    
    

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["name", "bio", "profile_picture", "birth_date"]