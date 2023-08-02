"""
Test for venue APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Venue

from venue.serializers import VenueSerializer

VENUES_URL = reverse('venue:venue-list')

# Esta helper function es porque tenemos que pasar el recipe ID a la URL. Cada
# detail será diferente, va a tener un UID para la recipe que queremos probar 
# Por eso creamos una función en ves de hacer hardcode
def detail_url(venue_id):
    """Create and return a venue detail URL"""
    return reverse('venue:venue-detail', args=[venue_id])


def create_venue(**params):
    '''
    Create and return a sample venue.
    '''
    defaults = {
        'name': 'Sample Venue',
        'address': 'Foo 123# Col. Barr',
        'city': 'Sample City',
        'state': 'Qux',
    }
    defaults.update(params)

    venue = Venue.objects.create(**defaults)
    return venue


def create_user(**params):
    '''
    Create and return a new user.
    '''
    return get_user_model().objects.create_user(**params)


# PUBLIC TESTS
class PublicVenueAPITests(TestCase):
    """Test unauthenticated API requests"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(VENUES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# PRIVATE TESTS
class PrivateVenueAPITests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.sales_employee = create_user(
            username = "john_doe",
            first_name = "John",
            fathers_name = "Doe",
            mothers_name = "Foo",
            email='john@example.com', 
            password='test123',
            role='sales',
        )

        self.tech_employee = create_user(
            username = "foo_barr",
            first_name = "Foo",
            fathers_name = "Barr",
            mothers_name = "Qux",
            email='foo@example.com', 
            password='test123',
            role='tech',
        )

        self.finance_employee = create_user(
            username = "jack_smith",
            first_name = "Jack",
            fathers_name = "Smith",
            mothers_name = "Don",
            email='jack@example.com', 
            password='test123',
            role='finance',
        )

        self.admin_employee = create_user(
            username = "tosin_abasi",
            first_name = "Tosin",
            fathers_name = "Abasi",
            mothers_name = "Nando",
            email='tosin@example.com', 
            password='test123',
            role='admin',
        )


    def test_retrieve_venues(self):
        '''
        Test retrieving a list of venues
        '''
        create_venue()

        self.client.force_authenticate(self.tech_employee)

        res = self.client.get(VENUES_URL)

        venues = Venue.objects.all().order_by('-id')
        serializer = VenueSerializer(venues, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_create_venue(self):
        '''
        Test creating a venue
        '''
        payload = {
            'name': 'Foo Theater',
            'address': 'P. Sherman #123',
            'city': 'Hamjam',
            'state': 'Testing',
        }

        # Only sales employees can have CUD permissions.
        self.client.force_authenticate(self.sales_employee)

        res = self.client.post(VENUES_URL, payload)


        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        venue = Venue.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(venue, k), v)


    def test_create_venue_without_permissions(self):
        '''
        Test user creating a venue without permissions
        '''
        payload = {
            'name': 'Foo Theater',
            'address': 'P. Sherman #123',
            'city': 'Hamjam',
            'state': 'Testing',
        }

        self.client.force_authenticate(self.tech_employee)

        res = self.client.post(VENUES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    def test_partial_update(self):
        '''
        Test partial update of a venue
        '''
        original_address = 'Foo 123# Col. Barr'
        venue = create_venue(
            name="Sample Venue"
        )

        payload = {'name': 'New Venue Name'}
        url = detail_url(venue.id)

        self.client.force_authenticate(self.sales_employee)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        venue.refresh_from_db()

        self.assertEqual(venue.name, payload['name'])
        self.assertEqual(venue.address, original_address)


    def test_full_update(self):
        '''
        Test full update of venue
        '''
        self.client.force_authenticate(self.sales_employee)

        venue = create_venue(
            name = "National Auditorium",
            address = "First Av #456",
            city = "Raccoon City",
            state = "Fire Nation",
        )

        payload = {
            'name': 'Metropolitan',
            'address': 'Sarabia #789',
            'city': 'Ba Sing Se',
            'state': 'Earch Nation',
        }

        url = detail_url(venue.id)

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        venue.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(venue, k), v)



    def test_delete_venue(self):
        '''
        Test deleting a venue successful.
        '''
        self.client.force_authenticate(self.sales_employee)

        venue = create_venue()
        
        url = detail_url(venue.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Venue.objects.filter(id=venue.id).exists())
