from django.urls import path

from .views import *

urlpatterns = [
    path("register/", RegisterCreateView.as_view(), name='register'),
    path("login/", LogInView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout')
]