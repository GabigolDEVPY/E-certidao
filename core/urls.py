from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from billing.views import StripeWebhookView


def google_site_verification(request):
    return HttpResponse(
        'google-site-verification: google971862346ff0bb4b.html\n',
        content_type='text/html; charset=utf-8',
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('google971862346ff0bb4b.html', google_site_verification, name='google_site_verification'),
    path('', include("home.urls")),
    path('users/', include("users.urls")),
    path('certidao/', include("certidao.urls")),
    path('billing/', include("billing.urls")),
    path('webhooks/stripe/', StripeWebhookView.as_view(), name='stripe_webhook_alternative'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
