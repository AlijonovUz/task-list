from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        username = self.fields['username']
        password1 = self.fields['password1']
        password2 = self.fields['password2']

        username.label = "Foydalanuvchi nomi"
        password1.label = "Parol"
        password2.label = "Parolni tasdiqlash"

        username.widget.attrs.update(
            {'class': "form-control rounded-md", 'placeholder': "Foydalanuvchi nomini kiriting"})
        password1.widget.attrs.update({'class': "form-control rounded-md", 'placeholder': "Parol kiriting"})
        password2.widget.attrs.update({'class': "form-control rounded-md", 'placeholder': "Parolni qayta kiriting"})

        username.error_messages[
            'unique'] = "Bu foydalanuvchi nomi allaqachon mavjud."


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        username = self.fields['username']
        password = self.fields['password']

        username.label = "Foydalanuvchi nomi"
        password.label = "Parol"

        username.widget.attrs.update(
            {'class': "form-control rounded-md", 'placeholder': "Foydalanuvchi nomini kiriting"})
        password.widget.attrs.update({'class': "form-control rounded-md", 'placeholder': "Parol kiriting"})

    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username:
            try:
                user = User.objects.get(username__iexact=username.lower())
                return user.username
            except User.DoesNotExist:
                return username
        
        return username