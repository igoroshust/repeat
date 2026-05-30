from django.contrib.auth.models import User # Модель
from django.views.generic.edit import CreateView # CreateView

from .forms import SignUpForm # Форма

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    success_url = 'registration/login.html'
    template_name = 'registration/signup.html'