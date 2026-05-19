from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
import re
from .models import User
from core.privacy import document_hash, email_hash, normalize_email


def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    def calcular_digito(cpf, peso):
        soma = sum(int(d) * p for d, p in zip(cpf, range(peso, 1, -1)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    digito1 = calcular_digito(cpf[:9], 10)
    digito2 = calcular_digito(cpf[:10], 11)

    return cpf[-2:] == f"{digito1}{digito2}"


def validar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)

    if len(cnpj) != 14:
        return False

    if cnpj == cnpj[0] * 14:
        return False

    def calcular_digito(cnpj, pesos):
        soma = sum(int(digito) * peso for digito, peso in zip(cnpj, pesos))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1

    digito1 = calcular_digito(cnpj[:12], pesos1)
    digito2 = calcular_digito(cnpj[:12] + str(digito1), pesos2)

    return cnpj[-2:] == f"{digito1}{digito2}"


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label="Nome")
    last_name  = forms.CharField(max_length=50, required=True, label="Sobrenome")
    aceite_privacidade = forms.BooleanField(
        required=True,
        label="Li e aceito a Política de Privacidade e o tratamento dos meus dados para criação da conta.",
        error_messages={"required": "Você precisa aceitar a Política de Privacidade para criar a conta."},
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "cpf_cnpj",
            "telefone",
            "password1",
            "password2",
            "aceite_privacidade",
        )

    def clean_email(self):
        email = normalize_email(self.cleaned_data.get('email'))

        if User.objects.filter(email_hash=email_hash(email)).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")

        return email

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        telefone_limpo = re.sub(r'\D', '', telefone)

        if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
            raise forms.ValidationError("Telefone inválido.")

        return telefone

    def clean_cpf_cnpj(self):
        cpf_cnpj = self.cleaned_data.get('cpf_cnpj')
        numeros = re.sub(r'\D', '', cpf_cnpj)

        if len(numeros) == 11:
            if not validar_cpf(numeros):
                raise forms.ValidationError("CPF inválido.")

        elif len(numeros) == 14:
            if not validar_cnpj(numeros):
                raise forms.ValidationError("CNPJ inválido.")

        else:
            raise forms.ValidationError("CPF (11 dígitos) ou CNPJ (14 dígitos) inválido.")

        if User.objects.filter(cpf_cnpj_hash=document_hash(numeros)).exists():
            raise forms.ValidationError("Este CPF/CNPJ já está em uso.")

        return cpf_cnpj


class EmailOrUsernameAuthenticationForm(forms.Form):
    username = forms.CharField(label="Usuário ou e-mail")
    password = forms.CharField(label="Senha", strip=False, widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": "Usuário, e-mail ou senha incorretos.",
        "inactive": "Esta conta está inativa.",
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        identifier = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if identifier and password:
            username = self._resolve_username(identifier)
            self.user_cache = authenticate(self.request, username=username, password=password)

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                )
            if not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages["inactive"], code="inactive")

        return self.cleaned_data

    def _resolve_username(self, identifier):
        identifier = identifier.strip()
        if "@" not in identifier:
            return identifier
        user = User.objects.filter(email_hash=email_hash(identifier)).only("username").first()
        return user.username if user else identifier

    def get_user(self):
        return self.user_cache
