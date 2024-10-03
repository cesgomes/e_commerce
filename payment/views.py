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
    """
    Handles the billing information process, including displaying the cart contents,
    and managing the billing form for both authenticated users and guests.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the billing information HTML page with cart details and billing form.
    """
    if request.method == "POST":
        # Get the cart instance for the current session
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        my_shipping = request.POST
        request.session['my_shipping']=my_shipping
        
        billing_form = PaymentForm()

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Render the billing info page with cart details and billing form for authenticated users
            return render(request, "payment/billing_info.html", {
                "cart_products": cart_products,
                "quantities": quantities,
                "shipping_info": request.POST,
                "billing_form": billing_form,
                "totals": totals
            })
        else:
            # Render the billing info page with cart details and billing form for guests
            return render(request, "payment/billing_info.html", {
                "cart_products": cart_products,
                "quantities": quantities,
                "shipping_info": request.POST,
                "billing_form": billing_form,
                "totals": totals
            })
    else:
        # If the request method is not POST, deny access and redirect to home
        messages.error(request, 'Access Denied')
        return redirect('home')

def process_order(request):
    if request.POST:
        payment_form = PaymentForm(request.POST or None)
        
        my_shipping=request.session.get('my_shipping')
        messages.success(request, "Order Placed")
        return redirect('home')
    else:
        messages.success(request, "Access Denied")
        return redirect('home')
        