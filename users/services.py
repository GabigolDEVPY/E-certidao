from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from certidao import services as pedido_services


def contexto_area_cliente(usuario):
    pedidos = pedido_services.pedidos_do_usuario(usuario)
    return {
        "pedidos": pedidos,
        "pedidos_pendentes": pedidos.filter(status="pendente"),
    }


def alterar_senha_usuario(request, senha_atual, nova_senha, confirmar_senha):
    user = request.user

    if not user.check_password(senha_atual):
        raise ValidationError("Senha atual incorreta.")
    if nova_senha != confirmar_senha:
        raise ValidationError("As senhas não coincidem.")

    validate_password(nova_senha, user=user)
    user.set_password(nova_senha)
    user.save()
    update_session_auth_hash(request, user)


def obter_pedido_para_pagamento(usuario, pedido_id):
    return pedido_services.obter_pedido_do_usuario(usuario, pedido_id)
