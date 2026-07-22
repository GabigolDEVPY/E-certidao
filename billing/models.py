from django.db import models
from django.db.models import Q


class Product(models.Model):
    """Produto cadastrado no sistema e vinculado ao Stripe."""

    TIPOS_CERTIDAO = [
        ('inteiro-teor', 'Certidão Inteiro Teor'),
        ('inteiro-teor-livro-03', 'Certidão Inteiro Teor - Livro 03'),
        ('onus-reais', 'Certidão de Busca CPF/CNPJ'),
        ('vintenaria', 'Certidão de Filiação de Domínio'),
        ('atualizada', 'Certidão Atualizada + Ônus Reais + Ações'),
    ]

    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, default='')
    tipo_certidao = models.CharField(
        max_length=50,
        choices=TIPOS_CERTIDAO,
        blank=True,
        default='',
        help_text='Tipo de certidão que usará este Price ID no checkout.',
    )

    # IDs do Stripe
    stripe_product_id = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text='ID do produto no Stripe (prod_xxx)',
    )
    stripe_price_id = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text='ID do preço no Stripe (price_xxx)',
    )

    preco = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        constraints = [
            models.UniqueConstraint(
                fields=['tipo_certidao'],
                condition=Q(ativo=True) & ~Q(tipo_certidao=''),
                name='unique_active_product_per_certidao',
            ),
        ]

    def __str__(self):
        tipo = self.get_tipo_certidao_display() if self.tipo_certidao else 'sem tipo'
        return f'{self.nome} ({tipo}) - R${self.preco}'


class Payment(models.Model):
    """Registro de pagamento vinculado a um pedido."""

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('falhou', 'Falhou'),
        ('cancelado', 'Cancelado'),
        ('reembolsado', 'Reembolsado'),
    ]

    pedido = models.OneToOneField(
        'certidao.OrderImovel',
        on_delete=models.CASCADE,
        related_name='payment',
    )

    stripe_checkout_session_id = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )
    stripe_payment_intent_id = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def __str__(self):
        return f'Pagamento #{self.id} - {self.status}'
