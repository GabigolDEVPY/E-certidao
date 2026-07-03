from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import OrderImovelForm
from .services import criar_pedido_imovel
from .models import Cartorio


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


def api_cidades(request):
    """Retorna lista de cidades únicas para um dado UF."""
    uf = request.GET.get('uf', '').strip().upper()
    if not uf:
        return JsonResponse({'cidades': []})
    cidades = (
        Cartorio.objects
        .filter(uf__iexact=uf)
        .values_list('cidade', flat=True)
        .distinct()
        .order_by('cidade')
    )
    return JsonResponse({'cidades': list(cidades)})


def api_cartorios(request):
    """Retorna lista de cartórios para uma dada cidade."""
    cidade = request.GET.get('cidade', '').strip()
    uf = request.GET.get('uf', '').strip().upper()
    if not cidade:
        return JsonResponse({'cartorios': []})
    qs = Cartorio.objects.filter(cidade__iexact=cidade)
    if uf:
        qs = qs.filter(uf__iexact=uf)
    cartorios = qs.values_list('nome', flat=True).order_by('nome')
    return JsonResponse({'cartorios': list(cartorios)})
