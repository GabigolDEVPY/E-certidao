import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from certidao.models import OrderImovel
from .services import criar_checkout_session, processar_evento_stripe

logger = logging.getLogger(__name__)


class CriarCheckoutView(LoginRequiredMixin, View):
    """Cria sessão de checkout no Stripe e redireciona o usuário."""
    login_url = 'login'

    def get(self, request, pedido_id):
        pedido = get_object_or_404(
            OrderImovel,
            id=pedido_id,
            usuario=request.user,
        )

        try:
            session = criar_checkout_session(pedido, request)
        except ImproperlyConfigured as exc:
            logger.warning('Checkout sem Price ID configurado: %s', exc)
            messages.error(
                request,
                'O valor deste tipo de certidão ainda não foi configurado. Entre em contato com o suporte.',
            )
            return redirect('certidao:imovel')

        return redirect(session.url)


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    """Recebe eventos do Stripe via webhook."""

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

        sucesso = processar_evento_stripe(payload, sig_header)

        if sucesso:
            return HttpResponse(status=200)
        return HttpResponse(status=400)


class CheckoutSucessoView(LoginRequiredMixin, View):
    """Página exibida após pagamento bem-sucedido."""
    login_url = 'login'

    def get(self, request):
        return render(request, 'billing/sucesso.html')


class CheckoutCanceladoView(LoginRequiredMixin, View):
    """Página exibida quando o pagamento é cancelado."""
    login_url = 'login'

    def get(self, request):
        return render(request, 'billing/cancelado.html')
