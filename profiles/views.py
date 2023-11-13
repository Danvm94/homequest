from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm
from checkout.models import Order
from properties.models import Property
from django.contrib import messages


# Create your views here.

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES,
                               instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    context = {
        'user': request.user,
        'form': form,
    }
    return render(request, 'profile.html', context)


@login_required
def contracts_view(request):
    user = request.user
    orders = Order.objects.filter(user_profile=user)

    context = {
        'orders': orders,
    }

    return render(request, 'contracts.html', context)


@login_required
def terminate_contract(request, property_id):
    user = request.user

    # Get the Order and Property objects or return a 404 if not found
    order = get_object_or_404(Order, property=property_id,
                              user_profile_id=user.pk)
    property_obj = get_object_or_404(Property, pk=property_id)

    # Delete the order
    order.delete()

    # Update the property object
    property_obj.gone = False
    property_obj.save()

    messages.success(request, 'You have now terminated the contract.')
    return redirect('home')
