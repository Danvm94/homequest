from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
import cloudinary.uploader
import cloudinary.api


# Create your models here.

class CustomUser(AbstractUser):
    picture = CloudinaryField(
        'image',
        default='homequest/media/profile',
        transformation=[
            {
                "width": 600,
                "height": 400,
                "crop": "crop",
                "format": "webp",
            }
        ],
        folder='homequest/media/'
    )

    def save(self, *args, **kwargs):
        # Check if the user already has a picture
        if self.pk:
            print(self.pk)
            # Retrieve the existing user to access their old picture
            existing_user = CustomUser.objects.get(pk=self.pk)
            if existing_user.picture:
                # Delete the old picture
                cloudinary.uploader.destroy(
                    public_id=existing_user.picture.public_id,
                    invalidate=True)
        super().save(*args, **kwargs)
