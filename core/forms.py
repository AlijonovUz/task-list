from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline']
        labels = {
            'title': "Vazifa nomi",
            'description': "Tafsilotlar",
            'deadline': "Muddati"
        }
        widgets = {
            'title': forms.TextInput(
                attrs={'class': "form-control rounded-md", 'placeholder': "Vazifa nomini kiriting"}),
            'description': forms.Textarea(
                attrs={'class': "form-control rounded-md", 'placeholder': "Vazifa haqida qo‘shimcha ma’lumot",
                       'rows': 4}),
            'deadline': forms.DateTimeInput(
                attrs={'class': "form-control rounded-md", 'type': "datetime-local", 'placeholder': "Vaqtni tanlang"},
                format='%Y-%m-%dT%H:%M'
            )
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

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')

        if not deadline:
            raise ValidationError("Iltimos, ushbu maydonni to'ldiring.")

        if self.instance.pk:
            old_deadline = self.instance.deadline
            if deadline < old_deadline:
                if deadline < timezone.now():
                    raise ValidationError("Vazifa muddati yaroqsiz.")
        else:
            if deadline < timezone.now():
                raise ValidationError("Vazifa muddati yaroqsiz.")
        return deadline

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].required = False
        self.fields['description'].required = False
        self.fields['deadline'].required = False
        self.fields['deadline'].input_formats = ['%Y-%m-%dT%H:%M']
