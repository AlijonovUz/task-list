from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.contrib import messages

from .forms import RegisterForm, LoginForm, ResendVerificationEmailForm
from .mixins import LoginNoRequiredMixin
from .utils import send_verification_email

User = get_user_model()


class RegisterCreateView(LoginNoRequiredMixin, CreateView):
    model = User
    form_class = RegisterForm
    template_name = "auth/register.html"

    def get_success_url(self):
        return reverse_lazy("check-email")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        send_verification_email(user, self.request)

        messages.success(
            self.request,
            "Ro'yxatdan o'tdingiz. Iltimos, elektron pochtangizni tasdiqlang!",
        )
        return super().form_valid(form)


class LogInView(LoginView):
    form_class = LoginForm
    template_name = "auth/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Tizimga kirdingiz.")
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "Tizimdan chiqdingiz.")
        return redirect("home")


class VerifyEmailView(LoginNoRequiredMixin, View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "Tasdiqlash linki yaroqsiz.")
            return redirect("check-email")

        if user.is_active:
            messages.info(request, "Sizning emailingiz allaqachon tasdiqlangan.")
            return redirect("login")

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, "Elektron pochta muvaffaqiyatli tasdiqlandi!")
            return redirect("login")

        messages.error(request, "Tasdiqlash linki yaroqsiz yoki muddati o'tgan.")
        return redirect("check-email")


class ResendVerificationEmailView(LoginNoRequiredMixin, View):
    def get(self, request):
        form = ResendVerificationEmailForm()
        return render(request, "auth/resend_verification.html", {"form": form})

    def post(self, request):
        form = ResendVerificationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email, is_active=False)
                send_verification_email(user, request)
                messages.success(request, "Tasdiqlash emaili qayta yuborildi.")
            except User.DoesNotExist:
                messages.error(
                    request,
                    "Bunday elektron pochtaga ega faollashtirilmagan foydalanuvchi topilmadi.",
                )
            return redirect("check-email")
        return render(request, "auth/resend_verification.html", {"form": form})


class CheckEmailView(LoginNoRequiredMixin, TemplateView):
    template_name = "auth/check-email.html"
