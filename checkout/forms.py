from django import forms
from .models import Order


class PropertyCheckoutRent(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('phone_number', 'delivery_address')
