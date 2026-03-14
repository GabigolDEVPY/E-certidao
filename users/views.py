from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")

class UserLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("")