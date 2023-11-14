from django.test import TestCase
from profiles.models import CustomUser
from .forms import PropertyCheckoutRent
from .models import Order, Property
from properties.models import State, RealEstateAgent


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
        order.save()
        self.assertEqual(Order.objects.count(), 1)


# models.py
class OrderModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = CustomUser.objects.create(username='testuser')
        agent = RealEstateAgent.objects.create(user_id=user.id)
        state = State.objects.create(state_name='Test')
        property_obj = Property.objects.create(
            title='Test Property',
            description='Test Description',
            address='Test Address',
            agent_id=agent.id,
            state=state,
            property_type='sale',
            price=1000,
            bathrooms=1,
            bedrooms=1,
            fireplaces=1,
            parking_spaces=1,
            size=100,
        )
        Order.objects.create(
            user_profile=user,
            property=property_obj,
            phone_number='1234567890',
            delivery_address='Test Address'
        )

    def test_user_profile(self):
        order = Order.objects.get(id=1)
        user_profile = order.user_profile
        self.assertEqual(user_profile.username, 'testuser')

    def test_property(self):
        order = Order.objects.get(id=1)
        property_obj = order.property
        self.assertEqual(property_obj.title, 'Test Property')

    def test_phone_number(self):
        order = Order.objects.get(id=1)
        phone_number = order.phone_number
        self.assertEqual(phone_number, '1234567890')

    def test_delivery_address(self):
        order = Order.objects.get(id=1)
        delivery_address = order.delivery_address
        self.assertEqual(delivery_address, 'Test Address')

    def test_date(self):
        order = Order.objects.get(id=1)
        # Ensure the date is not null
        self.assertIsNotNone(order.date)

    def test_stripe_pid(self):
        order = Order.objects.get(id=1)
        stripe_pid = order.stripe_pid
        # Ensure the default value is an empty string
        self.assertEqual(stripe_pid, '')
