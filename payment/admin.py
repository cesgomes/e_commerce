from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

#Register model in admin section
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

class OrderItemInline(admin.StackedInline):
    model=OrderItem
    
class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines=[OrderItemInline]
    
admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)