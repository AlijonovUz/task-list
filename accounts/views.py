from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib import messages

from .forms import RegisterForm, LoginForm
from .mixins import LoginNoRequiredMixin


class RegisterCreateView(LoginNoRequiredMixin, CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'auth/register.html'

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Ro'yxatdan o'tdingiz.")
        return super().form_valid(form)


class LogInView(LoginView):
    form_class = LoginForm
    template_name = 'auth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "Tizimga kirdingiz.")
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "Tizimdan chiqdingiz.")
        return redirect('home')
