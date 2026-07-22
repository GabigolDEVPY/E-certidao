import logging

import stripe
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction

from certidao.models import OrderImovel
from .models import Payment, Product

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


def criar_checkout_session(pedido, request):
    """Cria uma sessão de checkout no Stripe para o pedido."""

    product = Product.objects.filter(
        ativo=True,
        tipo_certidao=pedido.tipo_certidao,
    ).first()

    if not product or not product.stripe_price_id:
        raise ImproperlyConfigured(
            f'Configure um Product ativo com stripe_price_id para o tipo de certidão "{pedido.tipo_certidao}".'
        )

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': product.stripe_price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/billing/sucesso/') + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri('/billing/cancelado/'),
        metadata={
            'pedido_id': str(pedido.id),
            'tipo_certidao': pedido.tipo_certidao,
        },
    )

    Payment.objects.create(
        pedido=pedido,
        stripe_checkout_session_id=session.id,
        valor=product.preco,
        status='pendente',
    )

    return session


def processar_evento_stripe(payload, sig_header):
    """Valida e processa o evento recebido do Stripe via webhook."""

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        logger.error('Payload inválido recebido do Stripe.')
        return False
    except stripe.error.SignatureVerificationError:
        logger.error('Assinatura do webhook inválida.')
        return False

    if event['type'] == 'checkout.session.completed':
        try:
            _marcar_como_pago(event['data']['object'])
        except Exception:
            import traceback
            logger.exception('Erro ao processar checkout.session.completed:')
            try:
                with open('stripe_webhook_error.log', 'w', encoding='utf-8') as f:
                    traceback.print_exc(file=f)
            except Exception:
                pass
            return False

    return True


@transaction.atomic
def _marcar_como_pago(session_data):
    """Atualiza Payment e OrderImovel quando o pagamento é confirmado."""

    session_dict = session_data.to_dict() if hasattr(session_data, 'to_dict') else dict(session_data)

    session_id = session_dict.get('id') or ''
    payment_intent = session_dict.get('payment_intent') or ''
    metadata = session_dict.get('metadata') or {}
    pedido_id = metadata.get('pedido_id')

    if not pedido_id:
        logger.warning('Evento sem pedido_id nos metadata.')
        return

    try:
        payment = Payment.objects.select_related('pedido').get(
            stripe_checkout_session_id=session_id,
        )
    except Payment.DoesNotExist:
        logger.warning(f'Payment não encontrado para session {session_id}')
        return

    payment.stripe_payment_intent_id = payment_intent
    payment.status = 'pago'
    payment.save(update_fields=['stripe_payment_intent_id', 'status', 'atualizado_em'])

    pedido = payment.pedido
    pedido.is_paid = True
    pedido.status = 'pago'
    pedido.save(update_fields=['is_paid', 'status', 'atualizado_em'])

    logger.info(f'Pedido #{pedido_id} marcado como pago.')
