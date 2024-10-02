from django.urls import path
from . import views

# Definindo as URLs do aplicativo
urlpatterns = [
    # URL para a página de sucesso do pagamento
    # Esta URL mapeia para a função 'payment_success' na views.py
    # Quando o usuário acessa 'payment_success/', a função 'payment_success' será chamada
    path('payment_success/', views.payment_success, name="payment_success"),

    # URL para a página de checkout
    # Esta URL mapeia para a função 'checkout' na views.py
    # Quando o usuário acessa 'checkout/', a função 'checkout' será chamada
    path('checkout/', views.checkout, name="checkout"),
    path('billing_info/', views.billing_info, name="billing_info"),
]

