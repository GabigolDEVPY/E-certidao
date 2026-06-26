from django.contrib import admin

from .models import Product, Payment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'stripe_product_id', 'stripe_price_id', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'stripe_product_id')


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
