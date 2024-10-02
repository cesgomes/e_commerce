from django.db import models
from django.contrib.auth.models import User
from store.models import Product
class ShippingAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name=models.CharField(max_length=255)
    shipping_email = models.EmailField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=50, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=20, null=True, blank=True)
    shipping_country = models.CharField(max_length=100)
    
    #Dont plurarize address
    class Meta:
        verbose_name_plural = "Shipping Address"
        
    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    
# Create order Model (header)
class Order(models.Model):
    #Foreign key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shipping_address = models.CharField(max_length=1000)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'Order - {str(self.id)}'
    
# Create Order Items Model
class OrderItem(models.Model):
    #Foreign keys
    user = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def  __str__(self):
        return f'Order Item - {str(self.id)}'
    