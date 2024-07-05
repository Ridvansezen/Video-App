from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm
from .forms import UserLoginForm
from django.contrib.auth.models import User
from .models import Profile, UserModel
from .forms import ProfileForm, UserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Başarıyla kayıt olundu.')
                return redirect('index')
            else:
                messages.info(request, 'Giriş yapılamadı.')
        else:
            messages.info(request, 'Lütfen formu doğru doldurun.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'user/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Giriş başarılı.')
                return redirect('index')
            else:
                messages.error(request, 'Geçersiz kullanıcı adı veya parola.')
    else:
        form = UserLoginForm()
    
    return render(request, 'user/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('index')


@login_required
def request_user_profile(request):
    return redirect('user:view_profile', user_id=request.user.id)


def view_profile(request, user_id):
    profile_user = get_object_or_404(UserModel, pk=user_id)
    
    # Kullanıcıya ait profilin var olup olmadığını kontrol et, yoksa oluştur
    profile, created = Profile.objects.get_or_create(user=profile_user)

    if request.method == 'POST':
        if request.user == profile_user:  # Sadece kendi profili üzerinde değişiklik yapabilsin
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('user:view_profile', user_id=user_id)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user/profile.html', {'profile_user': profile_user, 'profile': profile, 'form': form})


def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profil başarıyla güncellendi.')
            return redirect('user:view_profile', user_id=request.user.id)
        else:
            messages.error(request, 'Formdaki bazı alanlar geçersiz.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'user/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

def change_password(request, user_id):
    user = get_object_or_404(UserModel, pk=user_id)

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Oturum açma hash'ini günceller
            messages.success(request, 'Şifreniz başarıyla değiştirildi!')
            return redirect('user:view_profile', user_id=user_id)
    else:
        form = PasswordChangeForm(user)

    return render(request, 'user/change_password.html', {'form': form})