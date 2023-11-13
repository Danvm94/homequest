from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from properties.models import Property
from django.views.decorators.http import require_POST
from homequest.settings import STRIPE_CLIENT_SECRET, STRIPE_PUBLIC_KEY, \
    STRIPE_CURRENCY
from .forms import PropertyCheckoutRent
from django.contrib.auth.decorators import login_required
import stripe
from .models import Order


# Create your views here.
@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = STRIPE_CLIENT_SECRET
        stripe.PaymentIntent.modify(pid, metadata={
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=e, status=400)


@login_required
def checkout_view(request, property_id):
    # Get the property object and current user
    property_object = Property.objects.get(id=property_id)
    if property_object.gone:
        messages.error(request,
                       'Sorry, this property is not available anymore')
        return redirect('home')

    # POST request
    if request.method == "POST":
        checkout_form = PropertyCheckoutRent(request.POST)
        if checkout_form.is_valid():
            pid = request.POST.get('client_secret').split('_secret')[0]
            checkout = checkout_form.save(commit=False)
            checkout.stripe_pid = pid
            checkout.property_id = property_object.pk
            checkout.save()
            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            # Change the property type to rented
            property_object = Property.objects.get(id=property_id)
            property_object.gone = True
            property_object.save()
            return redirect(reverse('checkout_success_view',
                                    args=[checkout.pk]))
    # GET request
    elif request.method == 'GET':
        # Stripe config
        stripe_public_key = STRIPE_PUBLIC_KEY
        stripe_total = round(property_object.price * 100)
        # Create a PaymentIntent
        stripe.api_key = STRIPE_CLIENT_SECRET
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=STRIPE_CURRENCY,
        )
        checkout_form = PropertyCheckoutRent()
        context = {
            'property': property_object,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'checkout_form': checkout_form,
        }
        # Render the checkout template
        return render(request, 'checkout.html', context=context)


@login_required
def checkout_success_view(request, primary_key):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    checkout = get_object_or_404(Order, pk=primary_key)
    user = request.user
    checkout.user_profile = user
    checkout.save()
    # Save the user's info
    if save_info:
        profile_data = {
            'default_phone_number': checkout.phone_number,
            'default_delivery_address': checkout.delivery_address,
        }
    messages.success(request, f'Order successfully processed! \
            Your order number is {primary_key}.')
    context = {
        'checkout': checkout,
    }
    return render(request, 'checkout_success.html', context)
