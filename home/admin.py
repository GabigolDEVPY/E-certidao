from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email_mascarado', 'telefone_mascarado', 'lida', 'criado_em')
    list_filter = ('lida', 'criado_em')
    readonly_fields = ('criado_em', 'atualizado_em')
    ordering = ('-criado_em',)


