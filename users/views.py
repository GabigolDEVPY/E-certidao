from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")

class UserLoginView(LoginView):
    template_name = "register.html"
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'login'
        context['login_form'] = context.get('form')  # renomeia o form de login
        context['form'] = RegisterForm()              # form de cadastro limpo
        return context
    
class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")  # era reverse_lazy("")
