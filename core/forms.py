from django import forms
from django.core.exceptions import ValidationError

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        labels = {
            'title': "Vazifa nomi",
            'description': "Tafsilotlar"
        }
        widgets = {
            'title': forms.TextInput(
                attrs={'class': "form-control rounded-md", 'placeholder': "Vazifa nomini kiriting"}),
            'description': forms.Textarea(
                attrs={'class': "form-control rounded-md", 'placeholder': "Vazifa haqida qo‘shimcha ma’lumot",
                       'rows': 4})
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if not title:
            raise ValidationError("Iltimos, ushbu maydonni to'ldiring.")

        task = Task.objects.filter(title=title, completed=False)
        if self.instance.pk:
            task = task.exclude(pk=self.instance.pk)

        if task.exists():
            raise ValidationError("Bunday sarlavhada faol vazifa mavjud.")

        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')

        if not description:
            raise ValidationError("Iltimos, ushbu maydonni to'ldiring.")
        return description

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].required = False
        self.fields['description'].required = False
