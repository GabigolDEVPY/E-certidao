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


class SeoMetadataTests(TestCase):
    def test_home_has_search_metadata(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, 'rel="canonical" href="https://certidaobr.com/"')
        self.assertContains(response, 'name="description"')
        self.assertContains(response, 'application/ld+json')
        self.assertContains(response, 'favicon-48x48.png')

    def test_home_links_to_blog_and_faq(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, reverse('blog_list'))
        self.assertContains(response, reverse('faq'))

    def test_home_contains_hidden_keyword_cluster(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, 'certidão de imóvel')
        self.assertContains(response, 'emitir certidão de imóvel')

    def test_robots_txt_points_to_sitemap_and_blocks_technical_paths(self):
        response = self.client.get(reverse('robots_txt'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sitemap: https://certidaobr.com/sitemap.xml')
        self.assertContains(response, 'Disallow: /admin/')
        self.assertContains(response, 'Disallow: /certidao/api/')

    def test_client_area_is_noindex(self):
        response = self.client.get(reverse('register'))

        self.assertContains(response, 'name="robots" content="noindex,nofollow"')
