from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label="Nome")
    last_name  = forms.CharField(max_length=50, required=True, label="Sobrenome")
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "cpf_cnpj",
            "telefone",
            "password1",
            "password2",
        )