from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class ImovelView(TemplateView):
    template_name = 'certidao_imovel.html'