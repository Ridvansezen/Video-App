from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django import forms
from .forms import CustomLoginForm

# Basit login formu
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


# Register view
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Kayıt sonrası otomatik login
            login(request, user)
            messages.success(request, f"Hoşgeldiniz, {user.username}!")  # Başarılı kayıt mesajı
            return redirect("/")  # index sayfasına yönlendir
    else:
        form = CustomUserCreationForm()
    return render(request, "user/register.html", {"form": form})


# Login view

def login_view(request):
    form = CustomLoginForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Hoşgeldiniz, {user.username}!")
            return redirect("/")
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı.")
    return render(request, "user/login.html", {"form": form})

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız.")
    return redirect("/")  # index sayfasına yönlendir


def index(request):
    return render(request, "index.html")