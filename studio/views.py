from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import LoginForm

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

    num_bad_logins=request.session.get('num_bad_logins', 0)

    if request.method == 'GET':
        form = LoginForm()
        return render(request,'studio/login.html', {'form': form})
    
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
            request.session['num_bad_logins'] = 0
        
        # form is not valid or user is not authenticated
        request.session['num_bad_logins'] = num_bad_logins+1
        return render(request,'studio/login.html',{'form': form, 'num_bad_logins': num_bad_logins})