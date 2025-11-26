from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('create/', TaskCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', TaskDetailView.as_view(), name='detail'),
    path('detail/<int:pk>/update/', TaskUpdateView.as_view(), name='update'),
    path('detail/<int:pk>/completed/', CompletedRedirectView.as_view(), name='completed'),
    path('detail/<int:pk>/delete/', TaskDeleteView.as_view(), name='delete'),
]