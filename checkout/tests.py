from django.test import TestCase
from .forms import PropertyCheckoutRent
from .models import Order


# forms.py
class PropertyCheckoutRentFormTests(TestCase):
    def test_valid_form(self):
        """
        Test if the form is valid with valid data.
        """
        data = {
            'phone_number': '1234567890',
            'delivery_address': '123 Main St, City'
        }
        form = PropertyCheckoutRent(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_phone_number(self):
        """
        Test if the form is invalid when phone_number is missing.
        """
        data = {
            'delivery_address': '123 Main St, City'
        }
        form = PropertyCheckoutRent(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)

    def test_invalid_form_missing_delivery_address(self):
        """
        Test if the form is invalid when delivery_address is missing.
        """
        data = {
            'phone_number': '1234567890',
        }
        form = PropertyCheckoutRent(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('delivery_address', form.errors)

    def test_invalid_form_empty_data(self):
        """
        Test if the form is invalid when all data is missing.
        """
        form = PropertyCheckoutRent(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertIn('delivery_address', form.errors)

    def test_form_save(self):
        """
        Test if the form saves the data to the Order model.
        """
        data = {
            'phone_number': '1234567890',
            'delivery_address': '123 Main St, City'
        }
        form = PropertyCheckoutRent(data=data)
        self.assertTrue(form.is_valid())
        order = form.save(commit=False)
        # Assuming you have a ForeignKey 'property' in Order model,
        # you can set it here before saving the order.
        # order.property = your_property_instance
        order.save()
        self.assertEqual(Order.objects.count(), 1)
