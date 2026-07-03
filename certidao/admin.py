from django.contrib import admin
from .models import OrderImovel, Cartorio

@admin.register(OrderImovel)
class OrderImovelAdmin(admin.ModelAdmin):
    list_display = (
        'nome_solicitante',
        'tipo_certidao',
        'estado',
        'cidade',
        'tipo_busca',
        'criado_em',
        'is_paid',
    )
    list_filter = ('tipo_certidao', 'is_paid', 'criado_em', 'atualizado_em')
    search_fields = ('nome_solicitante', 'email', 'estado', 'cidade', 'matriculas')
    ordering = ('-criado_em',)

@admin.register(Cartorio)
class CartorioAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'cidade',
        'uf',
    )