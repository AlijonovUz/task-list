import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class ResendVerificationEmailForm(forms.Form):
    email = forms.EmailField(
        label="Elektron pochta",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control rounded-md",
                "placeholder": "Elektron pochtangizni kiriting",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email, is_active=False).exists():
            raise forms.ValidationError(
                "Bunday emailga ega faollashtirilmagan foydalanuvchi topilmadi."
            )
        return email


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        username = self.fields["username"]
        email = self.fields["email"]
        password1 = self.fields["password1"]
        password2 = self.fields["password2"]

        username.label = "Foydalanuvchi nomi"
        email.label = "Elektron pochta"
        password1.label = "Parol"
        password2.label = "Parolni tasdiqlash"

        email.required = True

        username.widget.attrs.update(
            {
                "class": "form-control rounded-md",
                "placeholder": "Foydalanuvchi nomini kiriting",
            }
        )
        email.widget.attrs.update(
            {
                "class": "form-control rounded-md",
                "placeholder": "Elektron pochtani kiriting",
            }
        )
        password1.widget.attrs.update(
            {"class": "form-control rounded-md", "placeholder": "Parol kiriting"}
        )
        password2.widget.attrs.update(
            {
                "class": "form-control rounded-md",
                "placeholder": "Parolni qayta kiriting",
            }
        )

        username.error_messages["unique"] = "Bu foydalanuvchi nomi allaqachon mavjud."

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]{2,29}$", username):
            raise forms.ValidationError(
                "Foydalanuvchi nomi 3–30 ta belgidan iborat bo‘lishi kerak, "
                "harf yoki ostki chiziq bilan boshlanishi va faqat harflar, raqamlar yoki ostki chiziqlarni ishlatishi mumkin."
            )

        return username


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        username = self.fields["username"]
        password = self.fields["password"]

        username.label = "Foydalanuvchi nomi"
        password.label = "Parol"

        username.widget.attrs.update(
            {
                "class": "form-control rounded-md",
                "placeholder": "Foydalanuvchi nomini kiriting",
            }
        )
        password.widget.attrs.update(
            {"class": "form-control rounded-md", "placeholder": "Parol kiriting"}
        )

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if username:
            try:
                user = User.objects.get(username__iexact=username.lower())
                return user.username
            except User.DoesNotExist:
                return username

        return username
