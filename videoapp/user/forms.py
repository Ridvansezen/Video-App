from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import UserModel
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from user.models import Profile
from crispy_forms.layout import Layout, Submit, Field
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

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
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('bio', css_class='form-control')  # Etiketi burada CSS ile özelleştirebilirsiniz
        )

    class Meta:
        model = Profile
        fields = ['bio', 'profile_photo']


class UserEditForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'email', 'password']