from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = CloudinaryField('image', blank=False, null=False,
                                      default='')

    def save(self, *args, **kwargs):
        # Check if the user already has a profile picture
        if self.pk is not None:
            original = UserProfile.objects.get(pk=self.pk)
            if (original.profile_picture and self.profile_picture !=
                    original.profile_picture):
                raise ValueError("A user can have only one profile picture.")
        super(UserProfile, self).save(*args, **kwargs)
