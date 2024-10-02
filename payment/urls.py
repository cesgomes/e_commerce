from django.urls import path
from . import views

# Definindo as URLs do aplicativo
urlpatterns = [
    # URL para a página de sucesso do pagamento
    path('payment_success/', views.payment_success, name="payment_success"),

    # URL para a página de checkout
    path('checkout/', views.checkout, name="checkout"),
]
