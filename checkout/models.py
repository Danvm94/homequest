from django.db import models
from properties.models import Property
from profiles.models import CustomUser


class Order(models.Model):
    user_profile = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,
                                     null=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL,
                                 null=True)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    delivery_address = models.CharField(max_length=80, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')
