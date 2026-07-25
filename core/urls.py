from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import FileResponse, Http404, HttpResponse
from django.urls import include, path, reverse
from billing.views import StripeWebhookView


FAVICON_FILES = {
    'favicon.ico': ('favicon.ico', 'image/x-icon'),
    'favicon-16x16.png': ('favicon-16x16.png', 'image/png'),
    'favicon-32x32.png': ('favicon-32x32.png', 'image/png'),
    'favicon-48x48.png': ('favicon-48x48.png', 'image/png'),
    'favicon-96x96.png': ('favicon-96x96.png', 'image/png'),
    'apple-touch-icon.png': ('apple-touch-icon.png', 'image/png'),
    'android-chrome-192x192.png': ('android-chrome-192x192.png', 'image/png'),
    'android-chrome-512x512.png': ('android-chrome-512x512.png', 'image/png'),
    'site.webmanifest': ('site.webmanifest', 'application/manifest+json'),
}


def favicon_asset(request, filename):
    asset = FAVICON_FILES.get(filename)
    if asset is None:
        raise Http404

    asset_path = settings.BASE_DIR / 'static' / asset[0]
    if not asset_path.exists():
        raise Http404

    response = FileResponse(asset_path.open('rb'), content_type=asset[1])
    response['Cache-Control'] = 'public, max-age=86400'
    return response


def google_site_verification(request):
    return HttpResponse(
        'google-site-verification: google971862346ff0bb4b.html\n',
        content_type='text/html; charset=utf-8',
    )


def _absolute_url(path):
    return f'{settings.SITE_URL}{path}'


def sitemap_xml(request):
    from home.models import BlogPost
    from home.seo_content import CERTIDAO_SERVICE_PAGES

    public_urls = [
        {'path': reverse('home'), 'priority': '1.0', 'changefreq': 'weekly'},
        {'path': reverse('blog_list'), 'priority': '0.8', 'changefreq': 'weekly'},
        {'path': reverse('faq'), 'priority': '0.8', 'changefreq': 'weekly'},
        {'path': reverse('contact'), 'priority': '0.6', 'changefreq': 'monthly'},
        {'path': reverse('privacy_policy'), 'priority': '0.3', 'changefreq': 'yearly'},
        {'path': reverse('terms_of_use'), 'priority': '0.3', 'changefreq': 'yearly'},
    ]
    public_urls.extend(
        {
            'path': reverse('certidao_service', kwargs={'slug': service['slug']}),
            'priority': '0.9',
            'changefreq': 'weekly',
        }
        for service in CERTIDAO_SERVICE_PAGES
    )
    public_urls.extend(
        {
            'path': reverse('blog_detail', kwargs={'slug': post.slug}),
            'priority': '0.7',
            'changefreq': 'monthly',
            'lastmod': post.updated_at.date().isoformat(),
        }
        for post in BlogPost.objects.filter(is_published=True).only('slug', 'updated_at')
    )
    entries = '\n'.join(
        '  <url>\n'
        f'    <loc>{_absolute_url(item["path"])}</loc>\n'
        f'    {"<lastmod>" + item["lastmod"] + "</lastmod>" if item.get("lastmod") else ""}\n'
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
        'Disallow: /admin/\n'
        'Disallow: /webhooks/\n'
        'Disallow: /billing/webhook/\n'
        'Disallow: /certidao/api/\n'
        f'Sitemap: {settings.SITE_URL}/sitemap.xml\n',
        content_type='text/plain; charset=utf-8',
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('google971862346ff0bb4b.html', google_site_verification, name='google_site_verification'),
    path('favicon.ico', favicon_asset, {'filename': 'favicon.ico'}, name='favicon_ico'),
    path('favicon-16x16.png', favicon_asset, {'filename': 'favicon-16x16.png'}, name='favicon_16'),
    path('favicon-32x32.png', favicon_asset, {'filename': 'favicon-32x32.png'}, name='favicon_32'),
    path('favicon-48x48.png', favicon_asset, {'filename': 'favicon-48x48.png'}, name='favicon_48'),
    path('favicon-96x96.png', favicon_asset, {'filename': 'favicon-96x96.png'}, name='favicon_96'),
    path('apple-touch-icon.png', favicon_asset, {'filename': 'apple-touch-icon.png'}, name='apple_touch_icon'),
    path('android-chrome-192x192.png', favicon_asset, {'filename': 'android-chrome-192x192.png'}, name='android_chrome_192'),
    path('android-chrome-512x512.png', favicon_asset, {'filename': 'android-chrome-512x512.png'}, name='android_chrome_512'),
    path('site.webmanifest', favicon_asset, {'filename': 'site.webmanifest'}, name='site_webmanifest'),
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
