from .models import UserProfile


def get_profile_picture(user):
    try:
        profile_picture = UserProfile.objects.get(
            user=user).profile_picture
    except:
        profile_picture = 'homequest/media/profile'
    return profile_picture
