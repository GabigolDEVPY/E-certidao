from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path, reverse
from billing.views import StripeWebhookView


def google_site_verification(request):
    return HttpResponse(
        'google-site-verification: google971862346ff0bb4b.html\n',
        content_type='text/html; charset=utf-8',
    )


def _absolute_url(path):
    return f'{settings.SITE_URL}{path}'


def sitemap_xml(request):
    public_urls = [
        {'path': reverse('home'), 'priority': '1.0', 'changefreq': 'weekly'},
        {'path': reverse('contact'), 'priority': '0.6', 'changefreq': 'monthly'},
        {'path': reverse('privacy_policy'), 'priority': '0.3', 'changefreq': 'yearly'},
        {'path': reverse('terms_of_use'), 'priority': '0.3', 'changefreq': 'yearly'},
    ]
    entries = '\n'.join(
        '  <url>\n'
        f'    <loc>{_absolute_url(item["path"])}</loc>\n'
        f'    <changefreq>{item["changefreq"]}</changefreq>\n'
        f'    <priority>{item["priority"]}</priority>\n'
        '  </url>'
        for item in public_urls
    )
    return HttpResponse(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{entries}\n'
        '</urlset>\n',
        content_type='application/xml; charset=utf-8',
    )


def robots_txt(request):
    return HttpResponse(
        'User-agent: *\n'
        'Allow: /\n'
        f'Sitemap: {settings.SITE_URL}/sitemap.xml\n',
        content_type='text/plain; charset=utf-8',
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('google971862346ff0bb4b.html', google_site_verification, name='google_site_verification'),
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('', include("home.urls")),
    path('users/', include("users.urls")),
    path('certidao/', include("certidao.urls")),
    path('billing/', include("billing.urls")),
    path('webhooks/stripe/', StripeWebhookView.as_view(), name='stripe_webhook_alternative'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
