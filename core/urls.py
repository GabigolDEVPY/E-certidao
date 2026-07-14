from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from billing.views import StripeWebhookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("home.urls")),
    path('users/', include("users.urls")),
    path('certidao/', include("certidao.urls")),
    path('billing/', include("billing.urls")),
    path('webhooks/stripe/', StripeWebhookView.as_view(), name='stripe_webhook_alternative'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)