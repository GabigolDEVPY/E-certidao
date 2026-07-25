from django.contrib import admin

from .models import BlogPost, ContactMessage, FAQItem


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email_mascarado', 'telefone_mascarado', 'lida', 'criado_em')
    list_filter = ('lida', 'criado_em')
    readonly_fields = ('criado_em', 'atualizado_em')
    ordering = ('-criado_em',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'certidao_type', 'is_published', 'published_at', 'updated_at')
    list_filter = ('is_published', 'certidao_type', 'published_at')
    search_fields = ('title', 'excerpt', 'content', 'seo_keywords')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-published_at', '-created_at')


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'certidao_type', 'sort_order', 'is_published')
    list_filter = ('is_published', 'category', 'certidao_type')
    search_fields = ('question', 'answer')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('sort_order', 'question')


