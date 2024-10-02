from django.urls import path
from . import views

# Definindo as URLs do aplicativo
# Cada URL é mapeada para uma função específica no arquivo views.py
# Isso permite que o Django direcione as solicitações HTTP para a função correta

urlpatterns = [
    # URL para a página de sucesso do pagamento
    # Quando o usuário acessa 'payment_success/', a função 'payment_success' será chamada
    path('payment_success/', views.payment_success, name="payment_success"),

    # URL para a página de checkout
    # Quando o usuário acessa 'checkout/', a função 'checkout' será chamada
    path('checkout/', views.checkout, name="checkout"),

    # URL para a página de informações de cobrança
    # Quando o usuário acessa 'billing_info/', a função 'billing_info' será chamada
    path('billing_info/', views.billing_info, name="billing_info"),
]

# Notas de melhoria:
# 1. Certifique-se de que as funções referenciadas em views.py (payment_success, checkout, billing_info) estão implementadas corretamente.
# 2. Considere adicionar autenticação ou autorização nas views se necessário, para proteger as rotas.
# 3. Se o projeto crescer, pode ser útil organizar as URLs em diferentes arquivos de URL para cada aplicativo.
