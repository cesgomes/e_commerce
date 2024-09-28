from django.contrib import admin
from .models import Category, Costumer,Product, Order, Profile
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Costumer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)

#Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile
    
#Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username',
             'first_name',
             'last_name',
             'email',
             ]
    inlines = [ProfileInline]
    
#Unregister the Django Way
admin.site.unregister(User)

#Re-register the user with profile
admin.site.register(User, UserAdmin)