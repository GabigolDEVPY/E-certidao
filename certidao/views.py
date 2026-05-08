from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderImovelForm


class ImovelView(LoginRequiredMixin, View):
    template_name = 'certidao_imovel.html'
    login_url = 'login'

    def get(self, request):
        form = OrderImovelForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = OrderImovelForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.usuario = request.user
            order.save()
            messages.success(request, 'Pedido realizado com sucesso!')
            return redirect('area_cliente')
        return render(request, self.template_name, {'form': form})
