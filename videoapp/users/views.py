from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from users.forms import CustomUserCreationForm, CustomLoginForm, UserUpdateForm
from django import forms
from django.utils.html import format_html
from django.contrib.auth.decorators import login_required
from users.models import UserModel
from django.conf import settings

# Basit login formu
class LoginForm(forms.Form):
    username = forms.CharField(max_length=16)
    password = forms.CharField(widget=forms.PasswordInput)


# Register view
def register_view(request):
    # Kullanıcı zaten giriş yapmışsa
    if request.user.is_authenticated:
        messages.error(request, format_html('Önce çıkış yapmalısınız. <a href="{}">Buraya</a> tıklayarak çıkış yapabilirsiniz.', '/user/logout/'))
        return redirect("/")  # index sayfasına yönlendir

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Kayıt sonrası otomatik login
            login(request, user)
            messages.success(request, f"Başarıyla kayıt oldunuz. Hoşgeldiniz, {user.username}!")
            return redirect("/")  # index sayfasına yönlendir
    else:
        form = CustomUserCreationForm()
    return render(request, "user/register.html", {"form": form})


# Login view
def login_view(request):
    # Kullanıcı zaten giriş yapmışsa
    if request.user.is_authenticated:
        messages.error(request, format_html('Önce çıkış yapmalısınız. <a href="{}">Buraya</a> tıklayarak çıkış yapabilirsiniz.', '/user/logout/'))
        return redirect("/")

    form = CustomLoginForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Başarıyla giriş yaptınız. Hoşgeldiniz, {user.username}!")
            return redirect("/")
        else:
            # Hatalı giriş veya boş alan
            messages.error(request, "Kullanıcı adı veya şifre hatalı. Lütfen tüm alanları doldurun.")
    return render(request, "user/login.html", {"form": form})


# Logout view
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Başarıyla çıkış yaptınız.")
    else:
        messages.error(request, "Zaten giriş yapmamışsınız.")
    return redirect("login")




def index(request):
    return render(request, "index.html")



def profile_view(request, username):
    user_obj = get_object_or_404(UserModel, username=username)
    is_owner = request.user.is_authenticated and request.user.username == username

    if request.method == "POST" and is_owner:
        form = UserUpdateForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Profiliniz güncellendi.")
            return redirect("profile", username=username)
    else:
        form = UserUpdateForm(instance=user_obj)

    return render(request, "user/profile.html", {
        "user_obj": user_obj,
        "is_owner": is_owner,
        "form": form,
        "MEDIA_URL": settings.MEDIA_URL,
    })