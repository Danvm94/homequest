from django.test import TestCase, Client
from django.urls import reverse
from properties.models import \
    Property, RealEstateAgent, State
from profiles.models import CustomUser


class ViewsTest(TestCase):

    def setUp(self):
        # Create some test properties
        self.user = CustomUser.objects.create(username='testuser')
        self.agent = RealEstateAgent.objects.create(user_id=self.user.id)
        self.state = State.objects.create(state_name='Test')
        self.property1 = Property.objects.create(
            title='Test Property 1',
            description='Test Description',
            address='Test Address',
            agent_id=self.agent.id,
            state=self.state,
            property_type='sale',
            price=1000,
            bathrooms=1,
            bedrooms=1,
            fireplaces=1,
            parking_spaces=1,
            size=100,
        )
        self.property2 = Property.objects.create(
            title='Test Property 2',
            description='Test Description',
            address='Test Address',
            agent_id=self.agent.id,
            state=self.state,
            property_type='sale',
            price=1000,
            bathrooms=1,
            bedrooms=1,
            fireplaces=1,
            parking_spaces=1,
            size=100,
        )

        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('home'))

        # Assert that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains the expected template
        self.assertTemplateUsed(response, 'index.html')

        # Assert that the latest properties are present in the context
        self.assertIn('latest_properties', response.context)

        # Extract the IDs of the latest properties from the queryset
        actual_ids = [property_obj.id for property_obj in
                      response.context['latest_properties']]

        # Assert that the IDs match the expected values
        expected_ids = [self.property1.id, self.property2.id]
        self.assertListEqual(actual_ids, expected_ids)

    def test_about_view(self):
        response = self.client.get(reverse('about'))

        # Assert that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains the expected template
        self.assertTemplateUsed(response, 'about.html')

    def test_handler404_view(self):
        response = self.client.get('/nonexistentpage/')

        # Assert that the view returns a 404 status code
        self.assertEqual(response.status_code, 404)

        # Assert that the response contains the expected template
        self.assertTemplateUsed(response, '404.html')
