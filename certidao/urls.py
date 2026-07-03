from django.urls import path

from . views import ImovelView, api_cidades, api_cartorios

app_name = 'certidao'

urlpatterns = [
    path('imovel/', ImovelView.as_view(), name='imovel'),
    path('api/cidades/', api_cidades, name='api_cidades'),
    path('api/cartorios/', api_cartorios, name='api_cartorios'),
]