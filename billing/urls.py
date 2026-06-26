from django.urls import path

from .views import (
    CriarCheckoutView,
    StripeWebhookView,
    CheckoutSucessoView,
    CheckoutCanceladoView,
)

app_name = 'billing'

urlpatterns = [
    path(
        'checkout/<int:pedido_id>/',
        CriarCheckoutView.as_view(),
        name='criar_checkout',
    ),
    path('webhook/', StripeWebhookView.as_view(), name='stripe_webhook'),
    path('sucesso/', CheckoutSucessoView.as_view(), name='checkout_sucesso'),
    path('cancelado/', CheckoutCanceladoView.as_view(), name='checkout_cancelado'),
]
