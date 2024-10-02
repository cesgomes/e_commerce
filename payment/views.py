from django.shortcuts import render


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
    """
    Handles the checkout process by rendering the checkout page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered checkout page.
    """
    return render(request, "payment/checkout.html", {})
