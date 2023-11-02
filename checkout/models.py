from django.db import models
from django.db.models import Sum
from django.conf import settings

from properties.models import Property
from profiles.models import CustomUser


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(CustomUser, on_delete=models.SET_NULL)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    delivery_address = models.CharField(max_length=80, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')
