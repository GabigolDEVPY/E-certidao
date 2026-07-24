from django.db import models

from core.encrypted_fields import EncryptedCharField, EncryptedEmailField, EncryptedTextField
from core.privacy import mask_email, mask_phone


class ContactMessage(models.Model):
    nome = EncryptedCharField(max_length=255)
    email = EncryptedEmailField(max_length=254)
    telefone = EncryptedCharField(max_length=20)
    mensagem = EncryptedTextField()
    lida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Mensagem de contato'
        verbose_name_plural = 'Mensagens de contato'
        ordering = ['-criado_em']

    @property
    def email_mascarado(self):
        return mask_email(self.email)

    @property
    def telefone_mascarado(self):
        return mask_phone(self.telefone)

    def __str__(self):
        return f'{self.nome} - {self.criado_em:%d/%m/%Y %H:%M}'
