from django import forms
from .models import OrderImovel


class OrderImovelForm(forms.ModelForm):
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
        ]
        widgets = {
            'tipo_certidao': forms.HiddenInput(),
            'tipo_busca': forms.HiddenInput(),
            'matriculas': forms.HiddenInput(),
        }

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

        elif tipo_busca == 'endereco':
            for field in ['cep_imovel', 'numero_imovel', 'rua_imovel', 'bairro_imovel']:
                if not cleaned.get(field):
                    self.add_error(field, 'Este campo é obrigatório para busca por endereço.')

        return cleaned
