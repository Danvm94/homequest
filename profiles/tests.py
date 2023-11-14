from django.test import TestCase, Client
from django.urls import reverse
from .forms import ProfileEditForm
from .models import CustomUser
from checkout.models import Order
from properties.models import Property, RealEstateAgent, State
from django.contrib.auth import get_user_model


class CustomUserTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def tearDown(self):
        # Clean up resources, if any
        pass

    def test_picture_upload(self):
        # Check if the user has a picture
        self.assertIsNone(self.user.picture)

        # Set a picture for the user
        self.user.picture = 'path/to/test/image.jpg'
        self.user.save()

        # Retrieve the user again
        updated_user = get_user_model().objects.get(username='testuser')

        # Check if the URL of the picture field is as expected
        expected_url = ('https://res.cloudinary.com/djangoci/'
                        'image/upload/v1/path/to/test/image.jpg')
        self.assertEqual(updated_user.picture.url, expected_url)

    def test_picture_deletion_on_user_update(self):
        # Set a picture for the user
        self.assertIsNone(self.user.picture)

        # Set a picture for the user
        self.user.picture = 'path/to/test/image.jpg'
        self.user.save()

        # Retrieve the user again
        updated_user = get_user_model().objects.get(username='testuser')

        # Check if the public_id of the picture field is updated
        self.assertEqual(updated_user.picture.public_id,
                         'path/to/test/image')

    def test_picture_deletion_on_user_delete(self):
        # Set a picture for the user
        self.user.picture = 'path/to/test/image.jpg'
        self.user.save()

        # Delete the user
        self.user.delete()

        # Retrieve the user again
        deleted_user = get_user_model().objects.filter(
            username='testuser').first()

        # Check if the picture is deleted
        # (user should not be found, and thus picture should be None)
        self.assertIsNone(deleted_user)


class ProfileEditFormTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def tearDown(self):
        # Clean up resources, if any
        pass

    def test_form_valid_data(self):
        # Create a file to simulate image upload

        # Data to be submitted in the form
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
        }

        # Create form instance with the provided data and file
        form = ProfileEditForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Save the form data to the user model
        form.save(commit=False)
        self.user.first_name = form.cleaned_data['first_name']
        self.user.last_name = form.cleaned_data['last_name']
        self.user.save()

        # Retrieve the user again
        updated_user = CustomUser.objects.get(username='testuser')

        # Check if the user data is updated
        self.assertEqual(updated_user.first_name, 'John')
        self.assertEqual(updated_user.last_name, 'Doe')
        self.assertEqual(updated_user.picture, form.cleaned_data['picture'])

    def test_form_invalid_data(self):
        # Data with missing required fields
        form_data = {
            'first_name': '',
            'last_name': '',
        }

        # Create form instance with invalid data
        form = ProfileEditForm(data=form_data)

        # Check if the form is invalid
        self.assertFalse(form.is_valid())


class ProfileViewsTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_profile_view_get(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_view_post_valid_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
        }
        response = self.client.post(reverse('profile'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Successful redirect
        updated_user = CustomUser.objects.get(username='testuser')
        self.assertEqual(updated_user.first_name, 'John')
        self.assertEqual(updated_user.last_name, 'Doe')

    def test_profile_view_post_invalid_form(self):
        form_data = {
            'first_name': '',  # Invalid data
            'last_name': 'Doe',
        }
        response = self.client.post(reverse('profile'), data=form_data)
        self.assertEqual(response.status_code,
                         200)  # Form is not valid, stays on the same page
        self.assertFormError(response, 'form', 'first_name',
                             'This field is required.')

    def test_contracts_view(self):
        response = self.client.get(reverse('contracts_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contracts.html')

    def test_terminate_contract(self):
        agent = RealEstateAgent.objects.create(user_id=self.user.id)
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
        order = Order.objects.create(
            user_profile=self.user,
            property=property_obj,
            phone_number='1234567890',
            delivery_address='Test Address'
        )

        response = self.client.post(
            reverse('terminate_contract', args=[property_obj.id]))
        self.assertEqual(response.status_code, 302)  # Successful redirect
        self.assertFalse(Order.objects.filter(
            pk=order.pk).exists())  # Order should be deleted
        updated_property = Property.objects.get(pk=property_obj.id)
        self.assertFalse(
            updated_property.gone)  # Property 'gone' field should be False

    def test_terminate_contract_invalid_property_id(self):
        invalid_property_id = 999  # Assuming this ID doesn't exist
        response = self.client.post(
            reverse('terminate_contract', args=[invalid_property_id]))
        self.assertEqual(response.status_code,
                         404)  # Property not found, returns a 404
