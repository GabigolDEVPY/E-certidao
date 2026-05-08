from certidao import views
from django.urls import path
from .views import RegisterView, UserLoginView, UserLogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path("register/", RegisterView.as_view(), name="register"),

    path("login/", UserLoginView.as_view(), name="login"),

    path("logout/", UserLogoutView.as_view(), name="logout"),

    path('conta/', views.area_cliente, name='area_cliente'),

    path('conta/alterar-senha/', views.alterar_senha, name='alterar_senha'),
    path('conta/pedido/<int:pedido_id>/status/', views.alterar_status_pedido, name='alterar_status_pedido'),
    path('conta/pedido/<int:pedido_id>/pagar/', views.pagar_pedido, name='pagar_pedido'),

]