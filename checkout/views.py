from django.shortcuts import render
from properties.models import Property
from homequest.settings import STRIPE_CLIENT_SECRET, STRIPE_PUBLIC_KEY
from properties.utils import get_property_images


# Create your views here.
def checkout_view(request, property_id):
    # Get the property object
    property_object = Property.objects.get(id=property_id)
    property_object = get_property_images(property_object)

    context = {
        'property': property_object,
        'stripe_public_key': STRIPE_PUBLIC_KEY,
        'client_secret': STRIPE_CLIENT_SECRET
    }
    # Render the checkout template
    return render(request, 'checkout.html', context=context)
