from django.contrib import admin

from .models import Product, Payment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'tipo_certidao',
        'preco',
        'stripe_price_id',
        'ativo',
    )
    list_filter = ('ativo', 'tipo_certidao')
    search_fields = ('nome', 'stripe_product_id', 'stripe_price_id')
    fieldsets = (
        ('Tipo de certidão', {
            'fields': ('tipo_certidao', 'nome', 'descricao', 'ativo'),
            'description': 'Cadastre um produto ativo para cada tipo de certidão e preencha o Price ID correspondente.',
        }),
        ('Stripe', {
            'fields': ('stripe_product_id', 'stripe_price_id'),
        }),
        ('Preço', {
            'fields': ('preco',),
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'pedido',
        'valor',
        'status',
        'stripe_checkout_session_id',
        'criado_em',
    )
    list_filter = ('status', 'criado_em')
    search_fields = ('stripe_checkout_session_id', 'stripe_payment_intent_id')
    readonly_fields = (
        'stripe_checkout_session_id',
        'stripe_payment_intent_id',
        'criado_em',
        'atualizado_em',
    )
