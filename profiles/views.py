from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def profile_view(request):
    # Get the logged-in user
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)
