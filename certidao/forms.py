from django import forms
from .models import OrderImovel
import re

from core.privacy import normalize_email, only_digits


class OrderImovelForm(forms.ModelForm):
    aceite_tratamento = forms.BooleanField(
        required=True,
        label="Confirmo que os dados informados estão corretos e aceito o tratamento necessário para emitir a certidão.",
        error_messages={"required": "Confirme o tratamento dos dados para continuar o pedido."},
    )

    class Meta:
        model = OrderImovel
        fields = [
            'tipo_certidao',
            'estado', 'cidade', 'cartorio',
            'nome_solicitante', 'email', 'telefone',
            'tipo_busca', 'tipo_identificacao', 'matriculas',
            'cep_imovel', 'numero_imovel', 'rua_imovel',
            'bairro_imovel', 'complemento_imovel',
            'destino_utilizacao',
            'pais', 'cep', 'bairro', 'rua', 'numero', 'complemento',
            'aceite_tratamento',
        ]
        widgets = {
            'tipo_certidao': forms.HiddenInput(),
            'tipo_busca': forms.HiddenInput(),
            'matriculas': forms.HiddenInput(),
        }

    def clean_email(self):
        return normalize_email(self.cleaned_data.get('email'))

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        digits = only_digits(telefone)
        if len(digits) not in (10, 11):
            raise forms.ValidationError("Telefone inválido.")
        return telefone

    def clean_matriculas(self):
        value = self.cleaned_data.get('matriculas')
        if not value:
            return value

        matriculas = [item.strip() for item in value.split(',') if item.strip()]
        invalidas = [
            item for item in matriculas
            if len(item) > 30 or not re.match(r"^[0-9A-Za-z./-]+$", item)
        ]
        if invalidas:
            raise forms.ValidationError("Use apenas letras, números, ponto, barra ou hífen nas matrículas.")
        return ",".join(matriculas)

    def clean_cep(self):
        return self._clean_optional_cep('cep')

    def clean_cep_imovel(self):
        return self._clean_optional_cep('cep_imovel')

    def _clean_optional_cep(self, field_name):
        value = self.cleaned_data.get(field_name)
        if not value:
            return value
        if len(only_digits(value)) != 8:
            raise forms.ValidationError("CEP inválido.")
        return value

    def clean(self):
        cleaned = super().clean()
        tipo_busca = cleaned.get('tipo_busca')

        if not tipo_busca:
            self.add_error('tipo_busca', 'Selecione o tipo de busca do imóvel.')

        if tipo_busca == 'matricula':
            if not cleaned.get('tipo_identificacao'):
                self.add_error('tipo_identificacao', 'Selecione o tipo de identificação.')
            if not cleaned.get('matriculas'):
                self.add_error('matriculas', 'Adicione pelo menos uma matrícula ou transcrição.')
            for field in ['cep_imovel', 'numero_imovel', 'rua_imovel', 'bairro_imovel', 'complemento_imovel']:
                cleaned[field] = ''

        elif tipo_busca == 'endereco':
            for field in ['cep_imovel', 'numero_imovel', 'rua_imovel', 'bairro_imovel']:
                if not cleaned.get(field):
                    self.add_error(field, 'Este campo é obrigatório para busca por endereço.')
            cleaned['tipo_identificacao'] = None
            cleaned['matriculas'] = ''

        return cleaned
