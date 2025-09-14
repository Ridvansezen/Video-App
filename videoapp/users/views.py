from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from users.forms import CustomUserCreationForm, CustomLoginForm, UserUpdateForm, ChangeUsernameForm
from django import forms
from django.utils.html import format_html
from django.contrib.auth.decorators import login_required
from users.models import UserModel
from django.conf import settings
from posts.models import Post
from django.contrib.auth.forms import PasswordChangeForm


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
    return redirect("users:login")




def index(request):
    return render(request, "index.html")



def profile_view(request, username):
    user_obj = get_object_or_404(UserModel, username=username)
    is_owner = request.user.is_authenticated and request.user.username == username

    # Kullanıcıya ait postlar
    posts = Post.objects.filter(user=user_obj).order_by("-created_at")[:20]

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
        "posts": posts,  # burayı ekledik
    })
    
    
@login_required
def settings_view(request):
    if request.method == "POST":
        username_form = ChangeUsernameForm(request.POST, instance=request.user, prefix="username")
        password_form = PasswordChangeForm(user=request.user, data=request.POST, prefix="password")

        if "username-submit" in request.POST and username_form.is_valid():
            username_form.save()
            messages.success(request, "Kullanıcı adınız başarıyla değiştirildi.")
            return redirect("users:settings")

        if "password-submit" in request.POST and password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)  # login açık kalır
            messages.success(request, "Parolanız başarıyla değiştirildi.")
            return redirect("users:settings")

    else:
        username_form = ChangeUsernameForm(instance=request.user, prefix="username")
        password_form = PasswordChangeForm(user=request.user, prefix="password")

    return render(request, "user/settings.html", {
        "username_form": username_form,
        "password_form": password_form,
    })