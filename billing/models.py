from django.db import models


class Product(models.Model):
    """Produto cadastrado no sistema e vinculado ao Stripe."""

    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, default='')

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

    def __str__(self):
        return f'{self.nome} - R${self.preco}'


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
