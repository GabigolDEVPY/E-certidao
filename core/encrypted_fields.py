import base64
import hashlib

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models


ENCRYPTED_PREFIX = "enc:v1:"


def _load_fernet():
    try:
        from cryptography.fernet import Fernet
    except ImportError as exc:
        raise ImproperlyConfigured(
            "Instale a dependencia 'cryptography' para usar os campos criptografados."
        ) from exc

    configured_key = getattr(settings, "DATA_ENCRYPTION_KEY", "")
    if configured_key:
        raw_key = str(configured_key).encode("utf-8")
        try:
            return Fernet(raw_key)
        except ValueError:
            pass

    seed = configured_key or settings.SECRET_KEY
    derived_key = base64.urlsafe_b64encode(hashlib.sha256(str(seed).encode("utf-8")).digest())
    return Fernet(derived_key)


def encrypt_value(value):
    if value in (None, ""):
        return value
    text = str(value)
    if text.startswith(ENCRYPTED_PREFIX):
        return text
    token = _load_fernet().encrypt(text.encode("utf-8")).decode("ascii")
    return f"{ENCRYPTED_PREFIX}{token}"


def decrypt_value(value):
    if value in (None, ""):
        return value
    text = str(value)
    if not text.startswith(ENCRYPTED_PREFIX):
        return value

    try:
        token = text[len(ENCRYPTED_PREFIX):].encode("ascii")
        return _load_fernet().decrypt(token).decode("utf-8")
    except Exception as exc:
        raise ImproperlyConfigured(
            "Nao foi possivel descriptografar um campo protegido. Confira DATA_ENCRYPTION_KEY."
        ) from exc


class EncryptedTextField(models.TextField):
    description = "Texto criptografado em repouso"

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return encrypt_value(value)

    def from_db_value(self, value, expression, connection):
        return decrypt_value(value)

    def to_python(self, value):
        value = super().to_python(value)
        return decrypt_value(value)


class EncryptedCharField(EncryptedTextField):
    def __init__(self, *args, max_length=None, **kwargs):
        self.plaintext_max_length = max_length
        super().__init__(*args, max_length=max_length, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            "max_length": self.plaintext_max_length,
            "required": not self.blank,
            "widget": forms.TextInput,
        }
        defaults.update(kwargs)
        return forms.CharField(**defaults)


class EncryptedEmailField(EncryptedCharField):
    def formfield(self, **kwargs):
        defaults = {
            "max_length": self.plaintext_max_length,
            "required": not self.blank,
            "widget": forms.EmailInput,
        }
        defaults.update(kwargs)
        return forms.EmailField(**defaults)
