from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm
from .forms import UserLoginForm

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kayıt işlemi başarılı.')
            return redirect('user:login_user')
        else:
            messages.error(request, 'Lütfen formu doğru doldurun.')
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
        
