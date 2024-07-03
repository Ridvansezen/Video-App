from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm
from .forms import UserLoginForm
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm

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


def request_user_profile(request):
    return render(request, "user/profile.html")


def view_profile(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    profile = get_object_or_404(Profile, user=profile_user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile', user_id=user_id)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user/profile.html', {'profile_user': profile_user, 'profile': profile, 'form': form})        
