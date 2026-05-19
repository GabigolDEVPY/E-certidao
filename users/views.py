from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import EmailOrUsernameAuthenticationForm, RegisterForm
from .models import User
from . import services as user_services
from certidao import services as pedido_services


# ═══════════════════════════════════════════
# Autenticação
# ═══════════════════════════════════════════

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")


class UserLoginView(LoginView):
    template_name = "register.html"
    authentication_form = EmailOrUsernameAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'login'
        context['login_form'] = context.get('form')  # renomeia o form de login
        context['form'] = RegisterForm()              # form de cadastro limpo
        return context


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")


# ═══════════════════════════════════════════
# Área do Consumidor
# ═══════════════════════════════════════════

@login_required
def area_cliente(request):
    return render(request, 'user_area.html', user_services.contexto_area_cliente(request.user))


@login_required
@require_POST
def alterar_senha(request):
    senha_atual = request.POST.get('senha_atual', '')
    nova_senha = request.POST.get('nova_senha', '')
    confirmar_senha = request.POST.get('confirmar_senha', '')

    try:
        user_services.alterar_senha_usuario(request, senha_atual, nova_senha, confirmar_senha)
        messages.success(request, 'Senha alterada com sucesso.')
    except ValidationError as exc:
        messages.error(request, ' '.join(exc.messages))

    return redirect('area_cliente')


@login_required
@require_POST
def pagar_pedido(request, pedido_id):
    pedido = user_services.obter_pedido_para_pagamento(request.user, pedido_id)
    # TODO: Integrar gateway de pagamento
    messages.info(request, f'Funcionalidade de pagamento do pedido #{pedido.id} em desenvolvimento.')
    return redirect('area_cliente')


# ═══════════════════════════════════════════
# Área Administrativa (somente staff)
# ═══════════════════════════════════════════

@staff_member_required(login_url='login')
def admin_dashboard(request):
    status_filter = request.GET.get('status', '')

    return render(request, 'admin_area.html', {
        'pedidos': pedido_services.listar_pedidos_admin(status_filter),
        'contadores': pedido_services.contadores_pedidos(),
        'status_filter': status_filter,
        'status_choices': pedido_services.STATUS_CHOICES,
    })


@staff_member_required(login_url='login')
@require_POST
def admin_alterar_status(request, pedido_id):
    novo_status = request.POST.get('status', '')
    pedido = pedido_services.alterar_status_pedido(pedido_id, novo_status)

    if pedido is None:
        messages.error(request, 'Status inválido.')
    else:
        messages.success(request, f'Status do pedido #{pedido.id} atualizado para "{pedido.get_status_display()}".')

    return redirect('admin_dashboard')
