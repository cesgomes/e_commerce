from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products,
                                                 "quantities": quantities, 
                                                 "totals": totals})


def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # Test for post
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # Lookup product on database
        product = get_object_or_404(Product, id=product_id)
        # Save to session (cookie)
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()

        # Return response
        # response = JsonResponse({'Product Name': product.name})
        response = JsonResponse({'qty': cart_quantity})
        
        mensagem = f'Added 1 item to cart'
        if product_qty != 1:
            mensagem = f'Added {product_qty} itens to cart'
        messages.success(request, mensagem)
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        # Call delete Function in Cart
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        messages.success(request, "Item deleted from cart")
        # return redirect('cart_summary')
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty': product_qty})
        mensagem = 'Quantity updated for 1 item' if product_qty == 1 else f' Quantity updated for {product_qty} itens'
        messages.success(request, mensagem)
        return response
