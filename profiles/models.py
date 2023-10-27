from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField


# Create your models here.

class CustomUser(AbstractUser):
    picture = CloudinaryField('image', default='homequest/media/profile')
