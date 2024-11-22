from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import LoginForm
from django.core.cache import cache

def index(request):

    return render(
        request,
        'index.html',
        #context={'':,},
    )

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'studio/register.html', { 'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Вы успешно зарегестрировались')
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'studio/register.html', {'form': form})

def sign_in(request):

    if request.method == 'GET':
        form = LoginForm()
        if cache.get("num_bad_login", 0) < 2 or cache.get("num_bad_login", 0) == 3:
            return render(request,'studio/login.html', {'form': form})
        elif cache.get("num_bad_login", 0) == 2:
            cache.set("num_bad_login", 3, 120)
            return render(request,'studio/login_too_much.html')
        elif cache.get("num_bad_login", 0) >= 4:
            return render(request,'studio/blocked.html')
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Здравствуйте, {username.title()}')
                return redirect('index')
        
        # form is not valid or user is not authenticated
        cache.set("num_bad_login", (cache.get("num_bad_login", 0)+1), 120)
        if cache.get("num_bad_login", 0) < 2 or cache.get("num_bad_login", 0) == 3:
            return render(request,'studio/login.html', {'form': form})
        elif cache.get("num_bad_login", 0) == 2:
            cache.set("num_bad_login", 3, 120)
            return render(request,'studio/login_too_much.html')
        elif cache.get("num_bad_login", 0) >= 4:
            return render(request,'studio/blocked.html')