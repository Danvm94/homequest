from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm


# Create your views here.

@login_required
def profile_view(request):
    # Get the logged-in user
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
