from django.urls import path

from home.views import HomeView
from . views import ImovelView

app_name = 'certidao'

urlpatterns = [
    path('imovel', ImovelView.as_view(), name='imovel')
]