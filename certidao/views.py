from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import OrderImovelForm
from .services import criar_pedido_imovel
from .models import Cartorio, OrderImovel
from billing.models import Product


CERTIDAO_DESCRICOES = {
    'inteiro-teor': 'Certidão de Imóveis',
    'inteiro-teor-livro-03': 'Certidão de Registro Auxiliar',
    'onus-reais': 'Pesquisa positiva ou negativa de bens pelo CPF/CNPJ',
    'vintenaria': 'Certidão que retroage ao período necessário',
    'atualizada': 'Certidão de imóveis completa incluindo inteiro teor, ônus e ações',
}


def _format_brl(value):
    return f'R$ {value:.2f}'.replace('.', ',')


def _certidao_options(selected_tipo=''):
    produtos = {}
    for product in Product.objects.filter(ativo=True).exclude(tipo_certidao=''):
        produtos.setdefault(product.tipo_certidao, product)

    options = []
    for value, label in OrderImovel.TIPOS_CERTIDAO:
        product = produtos.get(value)
        configured = bool(product and product.stripe_price_id)
        options.append({
            'value': value,
            'title': label.upper(),
            'description': CERTIDAO_DESCRICOES.get(value, ''),
            'price_label': _format_brl(product.preco) if configured else 'Valor a configurar',
            'has_price': configured,
            'selected': selected_tipo == value or (not selected_tipo and value == 'inteiro-teor'),
        })
    return options


class ImovelView(LoginRequiredMixin, View):
    template_name = 'certidao_imovel.html'
    login_url = 'login'

    def get(self, request):
        form = OrderImovelForm()
        return render(request, self.template_name, self._context(form))

    def post(self, request):
        form = OrderImovelForm(request.POST)

        if form.is_valid():
            pedido = criar_pedido_imovel(form, request.user)
            return redirect('billing:criar_checkout', pedido_id=pedido.id)
        return render(request, self.template_name, self._context(form))

    def _context(self, form):
        return {
            'form': form,
            'certidao_options': _certidao_options(form['tipo_certidao'].value()),
        }


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
