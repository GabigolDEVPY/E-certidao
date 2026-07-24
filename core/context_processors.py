from django.conf import settings


def site_metadata(request):
    return {
        'site_url': settings.SITE_URL,
        'site_name': 'CertidaoBR',
    }
