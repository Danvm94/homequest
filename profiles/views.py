from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile


# Create your views here.

@login_required
def profile_view(request):
    # Get the logged-in user
    user = request.user
    try:
        user.profile_picture = UserProfile.objects.get(
            user=user).profile_picture
    except:
        user.profile_picture = 'homequest/media/57'
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)
