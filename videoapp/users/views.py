from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django import forms
from .forms import CustomLoginForm
from django.utils.html import format_html

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
