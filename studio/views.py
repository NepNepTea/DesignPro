from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login

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