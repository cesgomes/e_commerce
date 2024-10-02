from django.shortcuts import render
from cart.cart import Cart
from .forms import ShippingForm, ShippingAddress

def payment_success(request):
    """
    Handles the successful payment response.

    Args:
        request: The HTTP request object.

    Returns:
        [HttpResponse](https://docs.djangoproject.com/en/4.2/ref/request-response/#django.http.HttpResponse): Renders the payment success HTML page.
    """
    return render(request, "payment/payment_success.html", {})

def checkout(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    if request.user.is_authenticated:
        #Checkout as user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        #Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
    return render(request, "payment/checkout.html", {"cart_products": cart_products,
                                                    "quantities": quantities,
                                                    "shipping_form": shipping_form,
                                                    "totals": totals})
