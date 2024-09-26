from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_summary(request):
    return render(request, "cart_summary.html", {})


def cart_add(request):
    #Get the cart
    cart = Cart(request)
    #Test for post
    if request.POST.get('action') == 'post':
        #Get stuff
        product_id = int(request.POST.get('product_id'))
        #Lookup product on database
        product = get_object_or_404(Product,id=product_id)
        #Save to session (cookie)
        cart.add(product=product)
        
        # Get Cart Quantity
        cart_quantity = cart.__len__()                
        
        # Return response
        #response = JsonResponse({'Product Name': product.name})
        response = JsonResponse({'qty': cart_quantity})
        return response


def cart_delete(request):
    pass


def cart_update(request):
    pass
