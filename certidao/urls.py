from django.urls import path

from . views import ImovelView

app_name = 'certidao'

urlpatterns = [
    path('imovel/', ImovelView.as_view(), name='imovel'),
]