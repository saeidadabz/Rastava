from django.shortcuts import render

from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
# Create your views here.

class RegisterView(CreateView):
    template_name='registeration/register.html'
    form_class=CustomUserCreationForm
    success_url=reverse_lazy('login')
    

class LoginView(LoginView):
    template_name='registeration/login.html'

    def get_success_url(self) -> str:
        pass