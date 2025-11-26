from django.urls import path

from .views import *

urlpatterns = [
    path("register/", RegisterCreateView.as_view(), name="register"),
    path("login/", LogInView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "verify-email/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify-email"
    ),
    path(
        "resend-verification-email/",
        ResendVerificationEmailView.as_view(),
        name="resend-verification-email",
    ),
    path("check-email/", CheckEmailView.as_view(), name="check-email"),
]
