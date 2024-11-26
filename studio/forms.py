from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class PleaForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=1000)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    plan = forms.ImageField()

class ActivateUserForm(forms.Form):
    is_active = forms.BooleanField(initial=True, disabled=True)

class PleaCompleteForm(forms.Form):
    design = forms.ImageField()