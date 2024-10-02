from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class ShippingAddress(models.Model):
    # Relacionamento com o usuário, permitindo valores nulos e em branco
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    # Campos para armazenar informações de endereço de envio
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.EmailField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=50, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=20, null=True, blank=True)
    shipping_country = models.CharField(max_length=100)

    class Meta:
        # Define o nome plural da tabela no banco de dados
        verbose_name_plural = "Shipping Addresses"

    def __str__(self):
        # Representação em string do objeto
        return f'Shipping Address - {self.id}'


class Order(models.Model):
    # Relacionamento com o usuário, permitindo valores nulos e em branco
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    # Campos para armazenar informações do pedido
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=1000)
    amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2)  # Aumentado para 10 dígitos
    date_ordered = models.DateField(auto_now_add=True)

    class Meta:
        # Define o nome plural da tabela no banco de dados
        verbose_name_plural = "Orders"

    def __str__(self):
        # Representação em string do objeto
        return f'Order - {self.id}'


class OrderItem(models.Model):
    # Relacionamentos com Order, Product e User, permitindo valores nulos para Order e Product
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    # Campos para armazenar informações dos itens do pedido
    quantity = models.PositiveSmallIntegerField(default=1)
    # Aumentado para 10 dígitos
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        # Define o nome plural da tabela no banco de dados
        verbose_name_plural = "Order Items"

    def __str__(self):
        # Representação em string do objeto
        return f'Order Item - {self.id}'

    