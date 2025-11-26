from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.base import RedirectView

from .forms import TaskForm
from .models import Task


class HomeListView(ListView):
    paginate_by = 3
    template_name = "index.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            tasks = Task.objects.select_related("user").filter(user=self.request.user)

            status = self.request.GET.get("status")
            if status == "completed":
                tasks = tasks.filter(completed=True)
            elif status == "pending":
                tasks = tasks.filter(completed=False)
        else:
            tasks = Task.objects.none()
        return tasks


class TaskDetailView(DetailView):
    model = Task
    template_name = "detail.html"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Vazifa qo'shildi.")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"

    def form_valid(self, form):
        if form.has_changed():
            messages.success(self.request, "Vazifa tahrirlandi.")
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "delete.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Vazifa o'chirildi.")
        return super().form_valid(form)


class CompletedRedirectView(LoginRequiredMixin, RedirectView):
    pattern_name = "detail"

    def get_redirect_url(self, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"])
        if not task.completed:
            messages.success(self.request, "Vazifa bajarildi.")
            task.completed = True
            task.completed_at = timezone.now()
            task.save()
        return super().get_redirect_url(*args, **kwargs)
