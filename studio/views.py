from django.shortcuts import render
from .forms import RegisterForm

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