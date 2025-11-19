from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Task(models.Model):
    title = models.CharField(max_length=50, error_messages={'blank': "Iltimos, ushbu maydonni to'ldiring.",
                                                            'null': "Ushbu maydon bo'sh bo'la olmaydi."})
    description = models.TextField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})
