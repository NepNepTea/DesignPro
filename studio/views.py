from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import LoginForm
from django.core.cache import cache
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Plea
from .forms import PleaForm
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

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

def plea_create(request):
    if request.method == 'GET':
        form = PleaForm()
        return render(request, 'studio/plea_form.html', { 'form': form})
    if request.method == 'POST':
        form = PleaForm(request.POST, request.FILES) 
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            category = form.cleaned_data.get("category")
            if request.user.is_authenticated:
                username = request.user.username
            plan = form.cleaned_data.get("plan")
            obj = Plea.objects.create(name = name, description = description, category = category, plan = plan, author = User.objects.get(username = username))
            obj.save()
            messages.success(request, 'Вы успешно создали заявку')
            return redirect('index')
        else:
            return render(request, 'studio/plea_form.html', {'form': form})

class PleaDetailView(generic.DetailView):
    model = Plea


class PleaListView(LoginRequiredMixin,generic.ListView):
    model = Plea
    template_name ='studio/plea_list.html'

    def get_queryset(self):
        return Plea.objects.filter(author=self.request.user) #.filter(status__exact='o').order_by('due_back')

class PleaDelete(DeleteView):
    model = Plea
    success_url = reverse_lazy('pleas')