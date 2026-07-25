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


class BlogPost(models.Model):
    CERTIDAO_TYPES = [
        ('', 'Geral'),
        ('inteiro-teor', 'Certidão Inteiro Teor'),
        ('inteiro-teor-livro-03', 'Certidão Inteiro Teor - Livro 03'),
        ('onus-reais', 'Certidão de Busca CPF/CNPJ'),
        ('vintenaria', 'Certidão de Filiação de Domínio'),
        ('atualizada', 'Certidão Atualizada + Ônus Reais + Ações'),
    ]

    title = models.CharField('titulo', max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField('resumo', max_length=420)
    content = models.TextField('conteúdo')
    certidao_type = models.CharField(
        'tipo de certidão',
        max_length=50,
        choices=CERTIDAO_TYPES,
        blank=True,
        default='',
    )
    meta_description = models.CharField(max_length=180, blank=True, default='')
    seo_keywords = models.TextField('palavras-chave SEO', blank=True, default='')
    is_published = models.BooleanField('publicado', default=True)
    published_at = models.DateTimeField('publicado em', blank=True, null=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Post do blog'
        verbose_name_plural = 'Posts do blog'
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title


class FAQItem(models.Model):
    CERTIDAO_TYPES = BlogPost.CERTIDAO_TYPES

    question = models.CharField('pergunta', max_length=240)
    answer = models.TextField('resposta')
    certidao_type = models.CharField(
        'tipo de certidão',
        max_length=50,
        choices=CERTIDAO_TYPES,
        blank=True,
        default='',
    )
    category = models.CharField('categoria', max_length=120, blank=True, default='Certidão de imóvel')
    sort_order = models.PositiveIntegerField('ordem', default=0)
    is_published = models.BooleanField('publicado', default=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Pergunta frequente'
        verbose_name_plural = 'Perguntas frequentes'
        ordering = ['sort_order', 'question']

    def __str__(self):
        return self.question
