from django.contrib.auth.models import AbstractUser
from django.db import models

from core.encrypted_fields import EncryptedCharField, EncryptedEmailField
from core.privacy import document_hash, email_hash, mask_document, mask_email, mask_phone, normalize_email


class User(AbstractUser):
    first_name = EncryptedCharField(max_length=150, blank=True, verbose_name="first name")
    last_name = EncryptedCharField(max_length=150, blank=True, verbose_name="last name")
    cpf_cnpj = EncryptedCharField(max_length=18)
    cpf_cnpj_hash = models.CharField(max_length=64, unique=True, editable=False, null=True, blank=True)
    telefone = EncryptedCharField(max_length=20)
    email = EncryptedEmailField(max_length=254)
    email_hash = models.CharField(max_length=64, unique=True, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.email:
            self.email = normalize_email(self.email)
        self.email_hash = email_hash(self.email) if self.email else None
        self.cpf_cnpj_hash = document_hash(self.cpf_cnpj) if self.cpf_cnpj else None
        super().save(*args, **kwargs)

    @property
    def cpf_cnpj_mascarado(self):
        return mask_document(self.cpf_cnpj)

    @property
    def email_mascarado(self):
        return mask_email(self.email)

    @property
    def telefone_mascarado(self):
        return mask_phone(self.telefone)

    def __str__(self):
        return self.username
