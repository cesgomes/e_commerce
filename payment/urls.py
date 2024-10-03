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

    # URL para processar o pedido
    # Quando o usuário acessa 'process_order/', a função 'process_order' será chamada
    path('process_order/', views.process_order, name="process_order"),
]

# Notas de melhoria:
# 1. Certifique-se de que as funções referenciadas em views.py (payment_success, checkout, billing_info, process_order) estão implementadas corretamente.
# 2. Considere adicionar autenticação ou autorização nas views se necessário, para proteger as rotas.
#    - Por exemplo, você pode usar o decorator @login_required para garantir que apenas usuários autenticados acessem certas páginas.
# 3. Se o projeto crescer, pode ser útil organizar as URLs em diferentes arquivos de URL para cada aplicativo.
#    - Isso pode ser feito criando um arquivo urls.py em cada aplicativo e incluindo-os no urls.py principal do projeto.
# 4. Considere adicionar testes para garantir que cada URL está mapeando corretamente para a função desejada.
# 5. Se houver parâmetros dinâmicos nas URLs, como IDs de objetos, certifique-se de que eles estão sendo validados corretamente.
