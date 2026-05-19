from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import OrderImovel


STATUS_VALIDOS = [status for status, _label in OrderImovel.STATUS_PEDIDO]
STATUS_CHOICES = OrderImovel.STATUS_PEDIDO


@transaction.atomic
def criar_pedido_imovel(form, usuario):
    pedido = form.save(commit=False)
    pedido.usuario = usuario
    pedido.save()
    return pedido


def pedidos_do_usuario(usuario):
    return OrderImovel.objects.filter(usuario=usuario).order_by("-criado_em")


def pedidos_pendentes_do_usuario(usuario):
    return pedidos_do_usuario(usuario).filter(status="pendente")


def obter_pedido_do_usuario(usuario, pedido_id):
    return get_object_or_404(OrderImovel, id=pedido_id, usuario=usuario)


def listar_pedidos_admin(status_filter=""):
    pedidos = OrderImovel.objects.select_related("usuario").order_by("-criado_em")
    if status_filter in STATUS_VALIDOS:
        return pedidos.filter(status=status_filter)
    return pedidos


def contadores_pedidos():
    return {
        "total": OrderImovel.objects.count(),
        "pendente": OrderImovel.objects.filter(status="pendente").count(),
        "pago": OrderImovel.objects.filter(status="pago").count(),
        "enviado": OrderImovel.objects.filter(status="enviado").count(),
        "entregue": OrderImovel.objects.filter(status="entregue").count(),
        "cancelado": OrderImovel.objects.filter(status="cancelado").count(),
    }


def alterar_status_pedido(pedido_id, novo_status):
    if novo_status not in STATUS_VALIDOS:
        return None
    pedido = get_object_or_404(OrderImovel, id=pedido_id)
    pedido.status = novo_status
    pedido.save(update_fields=["status", "atualizado_em"])
    return pedido
