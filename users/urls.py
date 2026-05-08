from django.urls import path
from .views import RegisterView, UserLoginView, UserLogoutView
from . import views

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),

    # Área do consumidor
    path('conta/', views.area_cliente, name='area_cliente'),
    path('conta/alterar-senha/', views.alterar_senha, name='alterar_senha'),
    path('conta/pedido/<int:pedido_id>/pagar/', views.pagar_pedido, name='pagar_pedido'),

    # Área administrativa
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/pedido/<int:pedido_id>/status/', views.admin_alterar_status, name='admin_alterar_status'),
]