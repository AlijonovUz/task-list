from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.urls import reverse


class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    deadline = models.DateTimeField()
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_overdue(self):
        return not self.completed and timezone.now() > self.deadline

    @property
    def is_late(self):
        return self.completed_at and self.completed_at > self.deadline

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Vazifa '
        verbose_name_plural = 'Vazifalar'
        ordering = ['-created_at']
