from django.db import connection
from django.test import TestCase

from .forms import EmailOrUsernameAuthenticationForm
from .models import User


class UserPrivacyTests(TestCase):
    def test_sensitive_user_fields_are_encrypted_and_hashed(self):
        user = User.objects.create_user(
            username="joao",
            password="SenhaForte123!",
            email="JOAO@EXAMPLE.COM",
            cpf_cnpj="529.982.247-25",
            telefone="(11) 99999-9999",
            first_name="Joao",
            last_name="Silva",
        )

        with connection.cursor() as cursor:
            cursor.execute(
                "select email, cpf_cnpj, telefone, first_name, email_hash, cpf_cnpj_hash from users_user where id = %s",
                [user.id],
            )
            email, cpf_cnpj, telefone, first_name, email_hash, cpf_cnpj_hash = cursor.fetchone()

        self.assertTrue(email.startswith("enc:v1:"))
        self.assertTrue(cpf_cnpj.startswith("enc:v1:"))
        self.assertTrue(telefone.startswith("enc:v1:"))
        self.assertTrue(first_name.startswith("enc:v1:"))
        self.assertNotIn("joao@example.com", email)
        self.assertNotIn("52998224725", cpf_cnpj)
        self.assertEqual(len(email_hash), 64)
        self.assertEqual(len(cpf_cnpj_hash), 64)

        user.refresh_from_db()
        self.assertEqual(user.email, "joao@example.com")
        self.assertEqual(user.first_name, "Joao")

    def test_login_form_accepts_email_identifier(self):
        User.objects.create_user(
            username="maria",
            password="SenhaForte123!",
            email="maria@example.com",
            cpf_cnpj="11144477735",
            telefone="11988887777",
        )

        form = EmailOrUsernameAuthenticationForm(
            data={"username": "maria@example.com", "password": "SenhaForte123!"}
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.get_user().username, "maria")
