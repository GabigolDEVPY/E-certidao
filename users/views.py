from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from certidao.models import OrderImovel as Pedido


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
    

@login_required
def area_cliente(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-criado_em')
    pedidos_pendentes = pedidos.filter(status='pendente')
    return render(request, 'user_area.html', {
        'pedidos': pedidos,
        'pedidos_pendentes': pedidos_pendentes,
    })

@login_required
def alterar_senha(request):
    if request.method == 'POST':
        user = request.user
        if user.check_password(request.POST['senha_atual']):
            if request.POST['nova_senha'] == request.POST['confirmar_senha']:
                user.set_password(request.POST['nova_senha'])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Senha alterada com sucesso.')
            else:
                messages.error(request, 'As senhas não coincidem.')
        else:
            messages.error(request, 'Senha atual incorreta.')
    return redirect('area_cliente')

@login_required
def alterar_status_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
        pedido.status = request.POST['status']
        pedido.save()
        messages.success(request, f'Status do pedido #{pedido.id} atualizado.')
    return redirect('area_cliente')
    
@login_required
def pagar_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
        
        messages.success(request, f'Status do pedido #{pedido.id} atualizado.')
    return redirect('area_cliente')