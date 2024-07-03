from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import UserModel
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from user.models import Profile

UserModel = get_user_model()

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=25, min_length=3, help_text="Kullanıcı adı en az 3, en fazla 25 karakter olmalıdır.")

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Kayıt Ol'))

    def clean_username(self):
        username = self.cleaned_data['username']
        if not all(char.isalnum() or char in '._' for char in username):
            raise ValidationError(
                "Kullanıcı adı sadece harfler, rakamlar, '_' ve '.' karakterlerini içerebilir."
            )
        return username

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Giriş Yap'))
        
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_photo']
