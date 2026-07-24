from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['nome', 'email', 'telefone', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'field-input',
                'id': 'nome',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'field-input',
                'id': 'email',
                'required': True,
            }),
            'telefone': forms.TextInput(attrs={
                'id': 'telefone',
                'placeholder': '(00) 00000-0000',
                'maxlength': '15',
                'inputmode': 'numeric',
                'required': True,
            }),
            'mensagem': forms.Textarea(attrs={
                'class': 'field-input',
                'id': 'mensagem',
                'rows': 6,
                'required': True,
            }),
        }

    def clean_nome(self):
        return self.cleaned_data['nome'].strip()

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()

    def clean_telefone(self):
        return self.cleaned_data['telefone'].strip()

    def clean_mensagem(self):
        return self.cleaned_data['mensagem'].strip()
