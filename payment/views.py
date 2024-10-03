from django.shortcuts import render, get_object_or_404, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product


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

        # Store shipping information in session
        request.session['my_shipping'] = request.POST

        # Initialize the billing form
        billing_form = PaymentForm()

        # Render the billing info page with cart details and billing form
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
    """
    Processes the order by saving order details to the database and redirecting to home.

    Args:
        request: The HTTP request object containing order and session information.

    Returns:
        HttpResponse: Redirects to the home page after processing the order.
                      Displays an error message and redirects to checkout if shipping information is missing.
                      Displays an error message and redirects to home if the request method is not POST.
    """
    if request.method == "POST":
        # Get the cart instance for the current session
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Retrieve shipping information from session
        my_shipping = request.session.get('my_shipping')
        if not my_shipping:
            messages.error(request, "Shipping information is missing.")
            return redirect('checkout')

        # Extract shipping details
        full_name = my_shipping.get('shipping_full_name')
        email = my_shipping.get('shipping_email')
        shipping_address = (
            f"{my_shipping.get('shipping_address1')}\n"
            f"{my_shipping.get('shipping_address2')}\n"
            f"{my_shipping.get('shipping_city')}\n"
            f"{my_shipping.get('shipping_state')}\n"
            f"{my_shipping.get('shipping_zipcode')}\n"
            f"{my_shipping.get('shipping_country')}"
        )
        amount_paid = totals

        # Create an order instance
        create_order = Order(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            shipping_address=shipping_address,
            amount_paid=amount_paid
        )
        create_order.save()

        # Save each product in the order
        for product in cart_products():
            product_id = product.id
            price = product.sale_price if product.is_sale else product.price

            # Find the quantity for the current product
            quantity = quantities().get(str(product_id), 0)
            if quantity > 0:
                create_order_item = OrderItem(
                    order=create_order,
                    product=product,
                    user=request.user if request.user.is_authenticated else None,
                    quantity=quantity,
                    price=price
                )
                create_order_item.save()

        for key in list(request.session.keys()):
            if key == 'session_key':
                del request.session[key]
                
        messages.success(request, "Order Placed")
        return redirect('home')
    else:
        messages.error(request, "Access Denied")
        return redirect('home')