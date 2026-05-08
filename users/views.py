from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from .models import User
from certidao.models import OrderImovel as Pedido


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
    authentication_form = AuthenticationForm
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
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-criado_em')
    pedidos_pendentes = pedidos.filter(status='pendente')
    return render(request, 'user_area.html', {
        'pedidos': pedidos,
        'pedidos_pendentes': pedidos_pendentes,
    })


@login_required
@require_POST
def alterar_senha(request):
    user = request.user
    senha_atual = request.POST.get('senha_atual', '')
    nova_senha = request.POST.get('nova_senha', '')
    confirmar_senha = request.POST.get('confirmar_senha', '')

    if not user.check_password(senha_atual):
        messages.error(request, 'Senha atual incorreta.')
    elif len(nova_senha) < 8:
        messages.error(request, 'A nova senha deve ter no mínimo 8 caracteres.')
    elif nova_senha != confirmar_senha:
        messages.error(request, 'As senhas não coincidem.')
    else:
        user.set_password(nova_senha)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Senha alterada com sucesso.')

    return redirect('area_cliente')


@login_required
@require_POST
def pagar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    # TODO: Integrar gateway de pagamento
    messages.info(request, f'Funcionalidade de pagamento do pedido #{pedido.id} em desenvolvimento.')
    return redirect('area_cliente')


# ═══════════════════════════════════════════
# Área Administrativa (somente staff)
# ═══════════════════════════════════════════

STATUS_VALIDOS = [s[0] for s in Pedido.STATUS_PEDIDO]


@staff_member_required(login_url='login')
def admin_dashboard(request):
    status_filter = request.GET.get('status', '')
    pedidos = Pedido.objects.select_related('usuario').order_by('-criado_em')

    if status_filter and status_filter in STATUS_VALIDOS:
        pedidos = pedidos.filter(status=status_filter)

    contadores = {
        'total': Pedido.objects.count(),
        'pendente': Pedido.objects.filter(status='pendente').count(),
        'pago': Pedido.objects.filter(status='pago').count(),
        'enviado': Pedido.objects.filter(status='enviado').count(),
        'entregue': Pedido.objects.filter(status='entregue').count(),
        'cancelado': Pedido.objects.filter(status='cancelado').count(),
    }

    return render(request, 'admin_area.html', {
        'pedidos': pedidos,
        'contadores': contadores,
        'status_filter': status_filter,
        'status_choices': Pedido.STATUS_PEDIDO,
    })


@staff_member_required(login_url='login')
@require_POST
def admin_alterar_status(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    novo_status = request.POST.get('status', '')

    if novo_status not in STATUS_VALIDOS:
        messages.error(request, 'Status inválido.')
    else:
        pedido.status = novo_status
        pedido.save(update_fields=['status', 'atualizado_em'])
        messages.success(request, f'Status do pedido #{pedido.id} atualizado para "{pedido.get_status_display()}".')

    return redirect('admin_dashboard')