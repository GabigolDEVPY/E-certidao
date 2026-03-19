from django import forms
from django.contrib.auth.forms import UserCreationForm
import re
from .models import User


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

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
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

        return cpf_cnpj