from django.shortcuts import render, redirect
from .forms import RegisterForm, ActivateUserForm, PleaForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.cache import cache
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Plea, Category
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

def index(request):
    i_pleas = Plea.objects.filter(status='i')
    num_of_working_pleas = i_pleas.count()

    return render(
        request,
        'index.html',
        context={'num_of_working_pleas':num_of_working_pleas},
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
            user.is_active = False
            user.save()
            messages.success(request, ':ждите подтверждение от пользователя')
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
        return Plea.objects.filter(author=self.request.user).order_by('creationDate')#.filter(status='n')

class PleaDelete(DeleteView):
    model = Plea
    success_url = reverse_lazy('pleas')

class PleaListViewN(LoginRequiredMixin,generic.ListView):
    model = Plea
    template_name ='studio/plea_list_n.html'

    def get_queryset(self):
        return Plea.objects.filter(author=self.request.user).order_by('creationDate').filter(status='n')

class PleaListViewC(LoginRequiredMixin,generic.ListView):
    model = Plea
    template_name ='studio/plea_list_c.html'

    def get_queryset(self):
        return Plea.objects.filter(author=self.request.user).order_by('creationDate').filter(status='c')

class PleaListViewI(LoginRequiredMixin,generic.ListView):
    model = Plea
    template_name ='studio/plea_list_i.html'

    def get_queryset(self):
        return Plea.objects.filter(author=self.request.user).order_by('creationDate').filter(status='i')

class UserListView(LoginRequiredMixin,generic.ListView):
    model = User
    template_name ='studio/user_activation.html'

    def get_queryset(self):
        return User.objects.filter(is_active=False)

    
def activate_user(request, pk):
    inactive_user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':

        form = ActivateUserForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            inactive_user.is_active = form.cleaned_data['is_active']
            inactive_user.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('inactives') )

    else:
        form = ActivateUserForm()
        return render(request, 'studio/user_activate.html', {'form': form, 'inactive_user':inactive_user})

class CategoryListView(LoginRequiredMixin,generic.ListView):
    model = Category
    template_name ='studio/categorys.html'

class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('categorys')

class CategoryDetailView(generic.DetailView):
    model = Category

class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'