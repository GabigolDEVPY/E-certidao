from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage


class ContactViewTests(TestCase):
    def test_contact_post_creates_message(self):
        response = self.client.post(reverse('contact'), {
            'nome': 'Maria Silva',
            'email': 'maria@example.com',
            'telefone': '(11) 99999-9999',
            'mensagem': 'Preciso de ajuda com uma certidao.',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
        mensagem = ContactMessage.objects.get()
        self.assertEqual(mensagem.nome, 'Maria Silva')
        self.assertEqual(mensagem.email, 'maria@example.com')
        self.assertFalse(mensagem.lida)

    def test_contact_post_requires_valid_email(self):
        response = self.client.post(reverse('contact'), {
            'nome': 'Maria Silva',
            'email': 'email-invalido',
            'telefone': '(11) 99999-9999',
            'mensagem': 'Preciso de ajuda.',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
