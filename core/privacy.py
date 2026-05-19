import hashlib
import hmac
import re

from django.conf import settings


def only_digits(value):
    return re.sub(r"\D", "", value or "")


def normalize_email(value):
    return (value or "").strip().lower()


def normalize_document(value):
    return only_digits(value)


def _hash_key():
    key = (
        getattr(settings, "DATA_HASH_KEY", None)
        or getattr(settings, "DATA_ENCRYPTION_KEY", None)
        or settings.SECRET_KEY
    )
    return str(key).encode("utf-8")


def protected_hash(value):
    if value in (None, ""):
        return None
    normalized = str(value).strip().lower()
    return hmac.new(_hash_key(), normalized.encode("utf-8"), hashlib.sha256).hexdigest()


def email_hash(value):
    return protected_hash(normalize_email(value))


def document_hash(value):
    return protected_hash(normalize_document(value))


def mask_email(value):
    email = normalize_email(value)
    if "@" not in email:
        return email
    local, domain = email.split("@", 1)
    if len(local) <= 2:
        masked_local = local[:1] + "***"
    else:
        masked_local = f"{local[:2]}***{local[-1:]}"
    return f"{masked_local}@{domain}"


def mask_document(value):
    digits = only_digits(value)
    if len(digits) == 11:
        return f"***.{digits[3:6]}.{digits[6:9]}-**"
    if len(digits) == 14:
        return f"**.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-**"
    if len(digits) > 4:
        return f"***{digits[-4:]}"
    return "***"


def mask_phone(value):
    digits = only_digits(value)
    if len(digits) >= 4:
        return f"***{digits[-4:]}"
    return "***"
