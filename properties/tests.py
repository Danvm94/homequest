from django.test import TestCase, RequestFactory
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from profiles.models import CustomUser
from .models import RealEstateAgent, State, Property, Images
from .views import (properties_view, property_view, agents_view,
                    edit_property, delete_image_view, delete_property_view)


class RealEstateAgentModelTest(TestCase):

    def setUp(self):
        user = CustomUser.objects.create(
            username='test_user',
            email='test@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )
        self.agent = RealEstateAgent.objects.create(
            user=user,
            license_no='123456789',
            telephone_no='987654321'
        )

    def test_formatted_name(self):
        self.assertEqual(self.agent.formatted_name(), 'John Doe')

    def test_formatted_telephone(self):
        self.assertEqual(self.agent.formatted_telephone(), '(98) 7654-321')


class StateModelTest(TestCase):

    def setUp(self):
        self.state = State.objects.create(state_name='California')

    def test_str_method(self):
        self.assertEqual(str(self.state), 'California')


class PropertyModelTest(TestCase):

    def setUp(self):
        user = CustomUser.objects.create(
            username='test_user',
            email='test@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )
        agent = RealEstateAgent.objects.create(
            user=user,
            license_no='123456789',
            telephone_no='987654321'
        )
        state = State.objects.create(state_name='California')
        self.property = Property.objects.create(
            agent=agent,
            address='123 Main St',
            property_type='sale',
            state=state,
            description='Test property description',
            price=100000.00,
            title='Test Property',
            bathrooms=2,
            bedrooms=3,
            fireplaces=1,
            parking_spaces=2,
            size=150
        )

    def test_formatted_price_euro(self):
        self.assertEqual(self.property.formatted_price_euro(), '€100,000.00')

    def test_formatted_type(self):
        self.assertEqual(self.property.formatted_type(), 'FOR SALE')

    def test_formatted_size(self):
        self.assertEqual(self.property.formatted_size(), '150 m²')

    def test_formatted_state(self):
        self.assertEqual(self.property.formatted_state(), 'California')


class ImagesModelTest(TestCase):

    def setUp(self):
        user = CustomUser.objects.create(
            username='test_user',
            email='test@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )
        agent = RealEstateAgent.objects.create(
            user=user,
            license_no='123456789',
            telephone_no='987654321'
        )
        state = State.objects.create(state_name='California')
        property = Property.objects.create(
            agent=agent,
            address='123 Main St',
            property_type='sale',
            state=state,
            description='Test property description',
            price=100000.00,
            title='Test Property',
            bathrooms=2,
            bedrooms=3,
            fireplaces=1,
            parking_spaces=2,
            size=150
        )
        self.image = Images.objects.create(
            property=property,
            image='test_image.jpg'
        )

    def test_str_method(self):
        self.assertEqual(
            str(self.image), f"Image for Property: {self.image.property.pk}")


from django.test import TestCase
from .forms import PropertyFilterForm, ContactForm, PropertyForm, ImagesForm
from .models import State, RealEstateAgent


class PropertyFilterFormTest(TestCase):

    def setUp(self):
        user = CustomUser.objects.create(
            username='test_user',
            email='test@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )
        agent = RealEstateAgent.objects.create(
            user=user,
            license_no='123456789',
            telephone_no='987654321'
        )
        state = State.objects.create(state_name='California')
        self.property = Property.objects.create(
            agent=agent,
            address='123 Main St',
            property_type='sale',
            state=state,
            description='Test property description',
            price=100000.00,
            title='Test Property',
            bathrooms=2,
            bedrooms=3,
            fireplaces=1,
            parking_spaces=2,
            size=150
        )

    def test_form_valid_data(self):
        data = {
            'bedrooms': ['1', '2'],
            'bathrooms': ['3'],
            'parking': ['0', '1'],
            'min_price': '100000',
            'max_price': '200000',
            'min_size': '100',
            'max_size': '500',
            'clear_button': '',
        }
        form = PropertyFilterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_empty_data(self):
        form = PropertyFilterForm(data={})
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        data = {
            'bedrooms': ['6'],  # Invalid choice
        }
        form = PropertyFilterForm(data=data)
        self.assertFalse(form.is_valid())


class ContactFormTest(TestCase):

    def test_form_valid_data(self):
        data = {
            'subject': 'Test Subject',
            'message': 'This is a test message.',
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_empty_data(self):
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # Two required fields

    def test_form_invalid_data(self):
        data = {
            'subject': 'Short',
            'message': 'Short',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)  # Two fields with invalid data


class PropertyFormTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='test_user',
            email='test@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )
        self.agent = RealEstateAgent.objects.create(
            user=self.user,
            license_no='123456789',
            telephone_no='987654321'
        )
        self.state = State.objects.create(state_name='California')
        self.property = Property.objects.create(
            agent=self.agent,
            address='123 Main St',
            property_type='sale',
            state=self.state,
            description='Test property description',
            price=100000.00,
            title='Test Property',
            bathrooms=2,
            bedrooms=3,
            fireplaces=1,
            parking_spaces=2,
            size=150
        )

    def test_form_valid_data(self):
        data = {
            'title': 'Test Property',
            'address': '123 Main St',
            'state': self.state.id,
            'property_type': 'sale',
            'description': 'Test property description',
            'price': 100000.00,
            'bathrooms': 2,
            'bedrooms': 3,
            'fireplaces': 1,
            'parking_spaces': 2,
            'size': 150,
            'agent': self.agent.id,
        }
        form = PropertyForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_empty_data(self):
        form = PropertyForm(data={})
        self.assertFalse(form.is_valid())
