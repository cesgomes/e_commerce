from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Registra os modelos ShippingAddress, Order e OrderItem na seção de administração
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Define uma classe inline para exibir itens do pedido dentro do formulário de pedido


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0  # Não adiciona linhas extras por padrão

# Define uma classe de administração personalizada para o modelo Order


class OrderAdmin(admin.ModelAdmin):
    model = Order
    # Define 'date_ordered' como somente leitura
    readonly_fields = ['date_ordered']
    # fields = ['user', 'full_name']  # Descomente e ajuste se quiser listar apenas alguns campos
    inlines = [OrderItemInline]  # Adiciona a exibição inline de OrderItem


# Remove o registro padrão do modelo Order e registra novamente com a configuração personalizada
admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)
