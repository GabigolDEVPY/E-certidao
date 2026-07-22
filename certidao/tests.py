from django.db import connection
from django.test import TestCase

from users.models import User
from .forms import OrderImovelForm
from .models import OrderImovel


class OrderPrivacyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="cliente",
            password="SenhaForte123!",
            email="cliente@example.com",
            cpf_cnpj="52998224725",
            telefone="11999999999",
        )

    def test_order_sensitive_fields_are_encrypted_in_database(self):
        pedido = OrderImovel.objects.create(
            usuario=self.user,
            tipo_certidao="inteiro-teor",
            estado="SP - São Paulo",
            cidade="São Paulo",
            cartorio="1º Cartório de Registro de Imóveis",
            nome_solicitante="Cliente Teste",
            email="cliente@example.com",
            telefone="(11) 99999-9999",
            tipo_busca="matricula",
            tipo_identificacao="matricula",
            matriculas="123456",
            cpf_cnpj_busca="529.982.247-25",
            destino_utilizacao="Compra e venda",
        )

        with connection.cursor() as cursor:
            cursor.execute(
                "select nome_solicitante, email, telefone, matriculas, cpf_cnpj_busca, destino_utilizacao from certidao_orderimovel where id = %s",
                [pedido.id],
            )
            row = cursor.fetchone()

        for raw_value in row:
            self.assertTrue(raw_value.startswith("enc:v1:"))
        self.assertNotIn("Cliente Teste", "".join(row))
        self.assertNotIn("123456", "".join(row))

        pedido.refresh_from_db()
        self.assertEqual(pedido.nome_solicitante, "Cliente Teste")
        self.assertEqual(pedido.matriculas, "123456")
        self.assertEqual(pedido.cpf_cnpj_busca, "529.982.247-25")

    def test_order_form_does_not_require_delivery_address_for_email_delivery(self):
        form = OrderImovelForm(
            data={
                "tipo_certidao": "inteiro-teor",
                "estado": "SP - São Paulo",
                "cidade": "São Paulo",
                "cartorio": "1º Cartório de Registro de Imóveis",
                "nome_solicitante": "Cliente Teste",
                "email": "cliente@example.com",
                "telefone": "(11) 99999-9999",
                "tipo_busca": "matricula",
                "tipo_identificacao": "matricula",
                "matriculas": "123456",
                "destino_utilizacao": "Compra e venda",
                "pais": "Brasil",
                "aceite_tratamento": "on",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_cpf_cnpj_search_requires_valid_document_without_matricula(self):
        form = OrderImovelForm(
            data={
                "tipo_certidao": "onus-reais",
                "estado": "SP - São Paulo",
                "cidade": "São Paulo",
                "cartorio": "1º Cartório de Registro de Imóveis",
                "nome_solicitante": "Cliente Teste",
                "email": "cliente@example.com",
                "telefone": "(11) 99999-9999",
                "tipo_busca": "cpf_cnpj",
                "cpf_cnpj_busca": "529.982.247-25",
                "destino_utilizacao": "Pesquisa de bens",
                "pais": "Brasil",
                "aceite_tratamento": "on",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["tipo_busca"], "cpf_cnpj")
        self.assertEqual(form.cleaned_data["matriculas"], "")
        self.assertIsNone(form.cleaned_data["tipo_identificacao"])

    def test_cpf_cnpj_search_rejects_invalid_document(self):
        form = OrderImovelForm(
            data={
                "tipo_certidao": "onus-reais",
                "estado": "SP - São Paulo",
                "cidade": "São Paulo",
                "cartorio": "1º Cartório de Registro de Imóveis",
                "nome_solicitante": "Cliente Teste",
                "email": "cliente@example.com",
                "telefone": "(11) 99999-9999",
                "tipo_busca": "cpf_cnpj",
                "cpf_cnpj_busca": "111.111.111-11",
                "destino_utilizacao": "Pesquisa de bens",
                "pais": "Brasil",
                "aceite_tratamento": "on",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("cpf_cnpj_busca", form.errors)

    def test_filiacao_dominio_requires_anos_retroagir(self):
        data = {
            "tipo_certidao": "vintenaria",
            "estado": "SP - São Paulo",
            "cidade": "São Paulo",
            "cartorio": "1º Cartório de Registro de Imóveis",
            "nome_solicitante": "Cliente Teste",
            "email": "cliente@example.com",
            "telefone": "(11) 99999-9999",
            "tipo_busca": "matricula",
            "tipo_identificacao": "matricula",
            "matriculas": "123456",
            "destino_utilizacao": "Análise dominial",
            "pais": "Brasil",
            "aceite_tratamento": "on",
        }

        form = OrderImovelForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("anos_retroagir", form.errors)

        data["anos_retroagir"] = "20"
        form = OrderImovelForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_livro_03_accepts_registro_auxiliar(self):
        form = OrderImovelForm(
            data={
                "tipo_certidao": "inteiro-teor-livro-03",
                "estado": "SP - São Paulo",
                "cidade": "São Paulo",
                "cartorio": "1º Cartório de Registro de Imóveis",
                "nome_solicitante": "Cliente Teste",
                "email": "cliente@example.com",
                "telefone": "(11) 99999-9999",
                "tipo_busca": "matricula",
                "tipo_identificacao": "matricula",
                "matriculas": "RA-123456",
                "destino_utilizacao": "Registro auxiliar",
                "pais": "Brasil",
                "aceite_tratamento": "on",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
