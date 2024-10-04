from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from store.models import Profile
from datetime import datetime

def is_superuser(user):
    """Check if the user is a superuser."""
    return user.is_superuser

def payment_success(request):
    """Render the payment success page."""
    return render(request, "payment/payment_success.html")

def checkout(request):
    """
    Handle the checkout process.

    Retrieves the cart details and displays the checkout page with the shipping form.
    """
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user = get_object_or_404(ShippingAddress, user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        shipping_form = ShippingForm(request.POST or None)

    return render(request, "payment/checkout.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "shipping_form": shipping_form,
        "totals": totals
    })

def billing_info(request):
    """
    Handle the billing information process.

    Validates the request method and displays the billing information page.
    """
    if request.method != "POST":
        messages.error(request, 'Access Denied')
        return redirect('home')

    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    request.session['my_shipping'] = request.POST
    billing_form = PaymentForm()

    return render(request, "payment/billing_info.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "shipping_info": request.POST,
        "billing_form": billing_form,
        "totals": totals
    })

def process_order(request):
    """
    Process the order after billing information is submitted.

    Validates the request method, retrieves shipping information, creates an order,
    and clears the session.
    """
    if request.method != "POST":
        messages.error(request, "Access Denied")
        return redirect('home')

    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    my_shipping = request.session.get('my_shipping')
    if not my_shipping:
        messages.error(request, "Shipping information is missing.")
        return redirect('checkout')

    full_name = my_shipping.get('shipping_full_name')
    email = my_shipping.get('shipping_email')
    shipping_address = "\n".join([
        my_shipping.get('shipping_address1', ''),
        my_shipping.get('shipping_address2', ''),
        my_shipping.get('shipping_city', ''),
        my_shipping.get('shipping_state', ''),
        my_shipping.get('shipping_zipcode', ''),
        my_shipping.get('shipping_country', '')
    ])
    amount_paid = totals

    create_order = Order(
        user=request.user if request.user.is_authenticated else None,
        full_name=full_name,
        email=email,
        shipping_address=shipping_address,
        amount_paid=amount_paid
    )
    create_order.save()

    for product in cart_products():
        product_id = product.id
        price = product.sale_price if product.is_sale else product.price
        quantity = quantities().get(str(product_id), 0)
        if quantity > 0:
            OrderItem.objects.create(
                order=create_order,
                product=product,
                user=request.user if request.user.is_authenticated else None,
                quantity=quantity,
                price=price
            )

    # Clear session keys
    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]
            
    if request.user.is_authenticated:
        current_user = Profile.objects.filter(user__id=request.user.id)
        current_user.update(old_cart=None)
        
    messages.success(request, "Order Placed")
    return redirect('home')

@login_required
@user_passes_test(is_superuser)
def not_shipped_dash(request):
    """
    Display and update the dashboard for orders not yet shipped.

    Allows superusers to mark orders as shipped.
    """
    if request.method == "POST":
        num = request.POST['num']
        Order.objects.filter(id=num).update(shipped=True, date_shipped=datetime.now())
        messages.success(request, "Shipping Status updated")

    orders = Order.objects.filter(shipped=False)
    return render(request, 'payment/not_shipped_dash.html', {'orders': orders})

@login_required
@user_passes_test(is_superuser)
def shipped_dash(request):
    """
    Display and update the dashboard for shipped orders.

    Allows superusers to mark orders as not shipped.
    """
    if request.method == "POST":
        num = request.POST['num']
        Order.objects.filter(id=num).update(shipped=False, date_shipped=None)
        messages.success(request, "Shipping Status updated")

    orders = Order.objects.filter(shipped=True)
    return render(request, 'payment/shipped_dash.html', {'orders': orders})

@login_required
@user_passes_test(is_superuser)
def orders(request, pk):
    """
    Display and update the details of a specific order.

    Allows superusers to update the shipping status of an order.
    """
    order = get_object_or_404(Order, id=pk)
    order_items = OrderItem.objects.filter(order=pk)

    if request.method == "POST":
        status = request.POST['shipping_status']
        order.shipped = status.lower() == 'true'
        order.date_shipped = None if not order.shipped else order.date_shipped
        order.save()
        messages.success(request, "Shipping Status updated")
        return redirect('home')

    return render(request, 'payment/orders.html', {'order': order, 'items': order_items})