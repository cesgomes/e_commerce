from django.shortcuts import render
from cart.cart import Cart

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
    return render(request, "payment/checkout.html", {"cart_products": cart_products,
                                                 "quantities": quantities,
                                                 "totals": totals})

