from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm
from properties.utils import get_property_images
from checkout.models import Order


# Create your views here.

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    elif request.method == 'GET':
        form = ProfileEditForm(instance=request.user)
    context = {
        'user': user,
        'form': form,
    }
    return render(request, 'profile.html', context)


@login_required
def contracts_view(request):
    user = request.user
    orders = Order.objects.filter(user_profile=user)
    for order in orders:
        order.images = get_property_images(order.property).images

    context = {
        'orders': orders,
    }

    return render(request, 'contracts.html', context)

@login_required
def seize_contract(request, property_id):
    user = request.user
