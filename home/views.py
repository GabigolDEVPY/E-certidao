from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages

from .forms import ContactMessageForm
from .models import BlogPost, FAQItem
from .seo_content import CERTIDAO_SERVICE_PAGES, KEYWORD_CLUSTER, get_service_page


# Create your views here.
class HomeView(View):
    def get(self, request):
        context = {
            'service_pages': CERTIDAO_SERVICE_PAGES,
            'keyword_cluster': KEYWORD_CLUSTER,
        }
        return render(request, 'index.html', context)


class BlogListView(View):
    template_name = 'blog_list.html'

    def get(self, request):
        posts = BlogPost.objects.filter(is_published=True)
        query = request.GET.get('q', '').strip()
        if query:
            posts = posts.filter(
                Q(title__icontains=query)
                | Q(excerpt__icontains=query)
                | Q(content__icontains=query)
                | Q(seo_keywords__icontains=query)
            )

        return render(request, self.template_name, {
            'posts': posts,
            'query': query,
            'service_pages': CERTIDAO_SERVICE_PAGES,
            'keyword_cluster': KEYWORD_CLUSTER,
        })


class BlogDetailView(View):
    template_name = 'blog_detail.html'

    def get(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug, is_published=True)
        related_posts = (
            BlogPost.objects
            .filter(is_published=True)
            .exclude(id=post.id)
            .filter(Q(certidao_type=post.certidao_type) | Q(certidao_type=''))[:3]
        )
        related_faqs = FAQItem.objects.filter(
            is_published=True,
            certidao_type__in=[post.certidao_type, ''],
        )[:5]
        return render(request, self.template_name, {
            'post': post,
            'related_posts': related_posts,
            'related_faqs': related_faqs,
            'keyword_cluster': KEYWORD_CLUSTER,
        })


class FAQView(View):
    template_name = 'faq.html'

    def get(self, request):
        faqs = FAQItem.objects.filter(is_published=True)
        query = request.GET.get('q', '').strip()
        certidao_type = request.GET.get('tipo', '').strip()

        if certidao_type:
            faqs = faqs.filter(Q(certidao_type=certidao_type) | Q(certidao_type=''))
        if query:
            faqs = faqs.filter(Q(question__icontains=query) | Q(answer__icontains=query))

        return render(request, self.template_name, {
            'faqs': faqs,
            'query': query,
            'selected_tipo': certidao_type,
            'service_pages': CERTIDAO_SERVICE_PAGES,
            'keyword_cluster': KEYWORD_CLUSTER,
        })


class CertidaoServiceView(View):
    template_name = 'certidao_service.html'

    def get(self, request, slug):
        if slug == 'vintenaria':
            return redirect('certidao_service', slug='filiacao-de-dominio', permanent=True)

        service = get_service_page(slug)
        if service is None:
            raise Http404

        faqs = FAQItem.objects.filter(
            is_published=True,
            certidao_type__in=[service['tipo'], ''],
        )[:6]
        posts = BlogPost.objects.filter(
            is_published=True,
            certidao_type__in=[service['tipo'], ''],
        )[:3]

        return render(request, self.template_name, {
            'service': service,
            'service_pages': CERTIDAO_SERVICE_PAGES,
            'faqs': faqs,
            'posts': posts,
            'keyword_cluster': KEYWORD_CLUSTER,
        })


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'


class TermsOfUseView(TemplateView):
    template_name = 'terms_of_use.html'


class ContactView(View):
    template_name = 'contact_us.html'

    def get(self, request):
        return render(request, self.template_name, {'form': ContactMessageForm()})

    def post(self, request):
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensagem enviada com sucesso. Retornaremos o mais breve possivel.')
            return render(request, self.template_name, {'form': ContactMessageForm()})

        messages.error(request, 'Confira os campos destacados e tente novamente.')
        return render(request, self.template_name, {'form': form})
