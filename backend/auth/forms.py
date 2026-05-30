from django import forms # Формы
from django.contrib.auth.models import User # Модель
from django.contrib.auth.forms import UserCreationForm # UserCreationForm


class SignUpForm(UserCreationForm):
    """Регистрация пользователя"""
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Ваше имя')
    last_name = forms.CharField(label='Ваша фамилия')
    
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )