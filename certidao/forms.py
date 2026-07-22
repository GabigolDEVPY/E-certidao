from django import forms
from .models import OrderImovel
import re

from core.privacy import normalize_email, only_digits
from users.forms import validar_cnpj, validar_cpf


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
            'cpf_cnpj_busca', 'anos_retroagir',
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

    def clean_cpf_cnpj_busca(self):
        value = self.cleaned_data.get('cpf_cnpj_busca')
        if not value:
            return value

        digits = only_digits(value)
        if len(digits) == 11:
            if not validar_cpf(digits):
                raise forms.ValidationError("CPF inválido.")
        elif len(digits) == 14:
            if not validar_cnpj(digits):
                raise forms.ValidationError("CNPJ inválido.")
        else:
            raise forms.ValidationError("CPF (11 dígitos) ou CNPJ (14 dígitos) inválido.")

        return value

    def clean_anos_retroagir(self):
        value = self.cleaned_data.get('anos_retroagir')
        if value in (None, ''):
            return value
        if value < 1:
            raise forms.ValidationError("Informe uma quantidade de anos maior que zero.")
        if value > 200:
            raise forms.ValidationError("Informe uma quantidade de anos até 200.")
        return value

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
        tipo_certidao = cleaned.get('tipo_certidao')
        tipo_busca = cleaned.get('tipo_busca')
        certidoes_sem_endereco = {
            'inteiro-teor',
            'inteiro-teor-livro-03',
            'onus-reais',
            'vintenaria',
            'atualizada',
        }

        if not tipo_busca:
            self.add_error('tipo_busca', 'Selecione o tipo de busca do imóvel.')

        if tipo_certidao == 'onus-reais':
            cleaned['tipo_busca'] = 'cpf_cnpj'
            cleaned['tipo_identificacao'] = None
            cleaned['matriculas'] = ''
            cleaned['anos_retroagir'] = None
            if not cleaned.get('cpf_cnpj_busca'):
                self.add_error('cpf_cnpj_busca', 'Informe um CPF ou CNPJ válido.')
            for field in ['cep_imovel', 'numero_imovel', 'rua_imovel', 'bairro_imovel', 'complemento_imovel']:
                cleaned[field] = ''

        elif tipo_busca == 'matricula':
            cleaned['cpf_cnpj_busca'] = ''
            if tipo_certidao in certidoes_sem_endereco:
                cleaned['tipo_busca'] = 'matricula'
            if not cleaned.get('tipo_identificacao'):
                self.add_error('tipo_identificacao', 'Selecione o tipo de identificação.')
            if not cleaned.get('matriculas'):
                if tipo_certidao == 'inteiro-teor-livro-03':
                    self.add_error('matriculas', 'Adicione pelo menos um número de registro auxiliar.')
                else:
                    self.add_error('matriculas', 'Adicione pelo menos uma matrícula ou transcrição.')
            if tipo_certidao == 'vintenaria' and not cleaned.get('anos_retroagir'):
                self.add_error('anos_retroagir', 'Informe a quantidade de anos a retroagir.')
            elif tipo_certidao != 'vintenaria':
                cleaned['anos_retroagir'] = None
            for field in ['cep_imovel', 'numero_imovel', 'rua_imovel', 'bairro_imovel', 'complemento_imovel']:
                cleaned[field] = ''

        elif tipo_busca == 'endereco':
            if tipo_certidao in certidoes_sem_endereco:
                self.add_error('tipo_busca', 'Busca por endereço não está disponível para este tipo de certidão.')
            for field in ['cep_imovel', 'numero_imovel', 'rua_imovel', 'bairro_imovel']:
                if not cleaned.get(field):
                    self.add_error(field, 'Este campo é obrigatório para busca por endereço.')
            cleaned['tipo_identificacao'] = None
            cleaned['matriculas'] = ''
            cleaned['cpf_cnpj_busca'] = ''
            cleaned['anos_retroagir'] = None

        return cleaned
