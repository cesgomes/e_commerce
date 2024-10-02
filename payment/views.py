from django.shortcuts import render, get_object_or_404, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress
from django.contrib import messages

def payment_success(request):
    """
    Handles the successful payment response.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the payment success HTML page.
    """
    return render(request, "payment/payment_success.html", {})


def checkout(request):
    """
    Handles the checkout process, including displaying the cart contents,
    calculating totals, and managing the shipping form for both authenticated
    users and guests.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the checkout HTML page with cart details and shipping form.
    """
    # Get the cart instance for the current session
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # If authenticated, get the user's shipping address or return 404 if not found
        shipping_user = get_object_or_404(
            ShippingAddress, user__id=request.user.id)
        # Bind the shipping form to the user's shipping address
        shipping_form = ShippingForm(
            request.POST or None, instance=shipping_user)
    else:
        # If not authenticated, provide an empty shipping form for guest checkout
        shipping_form = ShippingForm(request.POST or None)

    # Render the checkout page with cart details and the shipping form
    return render(request, "payment/checkout.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "shipping_form": shipping_form,
        "totals": totals
    })
def billing_info(request):
    if request.POST: 
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        billing_form = PaymentForm()

        #Check to validate if user is logged in
        if request.user.is_authenticated:
            return render(request,
                          "payment/billing_info.html", {
                          "cart_products": cart_products,
                          "quantities": quantities,
                          "shipping_info": request.POST,
                          "billing_form": billing_form,
                          "totals": totals
        })
        else:
            #Not logged in
            return render(request,
                          "payment/billing_info.html", {
                              "cart_products": cart_products,
                              "quantities": quantities,
                              "shipping_info": request.POST,
                              "billing_form": billing_form,
                              "totals": totals
                          })

        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {
            "cart_products": cart_products,
            "quantities": quantities,
            "shipping_form": shipping_form,
            "totals": totals
        })
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')
