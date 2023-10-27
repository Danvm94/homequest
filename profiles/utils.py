from .models import UserProfile


def get_profile_image(user):
    try:
        user.profile_picture = UserProfile.objects.get(
            user=user).profile_picture
    except:
        user.profile_picture = None