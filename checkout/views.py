from django.shortcuts import render
from properties.models import Property
from homequest.settings import STRIPE_CLIENT_SECRET, STRIPE_PUBLIC_KEY, STRIPE_CURRENCY
from properties.utils import get_property_images
from .forms import PropertyCheckoutRent
from django.contrib.auth.decorators import login_required
import stripe


# Create your views here.
@login_required
def checkout_view(request, property_id):
    # Get the property object
    property_object = Property.objects.get(id=property_id)
    property_object = get_property_images(property_object)
    user = request.user

    # Stripe config
    stripe_public_key = STRIPE_PUBLIC_KEY
    stripe_total = round(property_object.price * 100)
    stripe.api_key = STRIPE_CLIENT_SECRET
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=STRIPE_CURRENCY,
    )

    checkout_form = PropertyCheckoutRent(
        request.POST, user_name=user.first_name, user_surname=user.last_name)

    context = {
        'property': property_object,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'checkout_form': checkout_form,
    }
    # Render the checkout template
    return render(request, 'checkout.html', context=context)
