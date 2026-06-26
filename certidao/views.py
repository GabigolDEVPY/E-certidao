from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderImovelForm
from .services import criar_pedido_imovel


class ImovelView(LoginRequiredMixin, View):
    template_name = 'certidao_imovel.html'
    login_url = 'login'

    def get(self, request):
        form = OrderImovelForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = OrderImovelForm(request.POST)

        if form.is_valid():
            pedido = criar_pedido_imovel(form, request.user)
            return redirect('billing:criar_checkout', pedido_id=pedido.id)
        return render(request, self.template_name, {'form': form})

