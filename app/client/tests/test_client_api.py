"""
Test for client APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Client

from client.serializers import ClientSerializer

CLIENT_URL = reverse('client:client-list')

# Esta helper function es porque tenemos que pasar el recipe ID a la URL. Cada
# detail será diferente, va a tener un UID para la recipe que queremos probar 
# Por eso creamos una función en ves de hacer hardcode
def detail_url(client_id):
    """Create and return a cli detail URL"""
    return reverse('client:client-detail', args=[client_id])


def create_client(**params):
    '''
    Create and return a sample client.
    '''
    defaults = {
        'name': 'Legolas Greenleaf',
        'phone': '5645651356',
        'email': 'legolas@example.com',
    }
    defaults.update(params)

    venue = Client.objects.create(**defaults)
    return venue


def create_user(**params):
    '''
    Create and return a new user.
    '''
    return get_user_model().objects.create_user(**params)


# PUBLIC TESTS
class PublicClientAPITests(TestCase):
    """Test unauthenticated API requests"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(CLIENT_URL)

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


    def test_retrieve_clients(self):
        '''
        Test retrieving a list of clients
        '''
        create_client()

        self.client.force_authenticate(self.tech_employee)

        res = self.client.get(CLIENT_URL)

        clients = Client.objects.all().order_by('-id')
        serializer = ClientSerializer(clients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_create_client(self):
        '''
        Test creating a client
        '''
        payload = {
            'name': 'Gimli Gloinson',
            'phone': '4456125865',
            'email': 'gimli@example.com',
        }

        # Only sales employees can have CUD permissions.
        self.client.force_authenticate(self.sales_employee)

        res = self.client.post(CLIENT_URL, payload)


        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        client = Client.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(client, k), v)


    def test_create_client_without_permissions(self):
        '''
        Test user creating a client without permissions
        '''
        payload = {
            'name': 'Aragorn Elessar',
            'phone': '3345265845',
            'email': 'aragorn@example.com',
        }

        self.client.force_authenticate(self.tech_employee)

        res = self.client.post(CLIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    def test_partial_update(self):
        '''
        Test partial update of a client
        '''
        self.client.force_authenticate(self.sales_employee)
        original_email = 'legolas@example.com'

        client = create_client(
            name="Frodo Baggins",
        )

        payload = {'name': 'Sam Gamgee'}
        url = detail_url(client.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        client.refresh_from_db()

        self.assertEqual(client.name, payload['name'])
        self.assertEqual(client.email, original_email)


    def test_full_update(self):
        '''
        Test full update of client
        '''
        self.client.force_authenticate(self.sales_employee)

        client = create_client(
            name = "Boromir Denethor",
            phone = "6645132568",
            email = "boromir@example.com",
        )

        payload = {
            'name': 'Faramir Denethor',
            'phone': '7745645315',
            'email': 'faramir@example.com',
        }

        url = detail_url(client.id)

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        client.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(client, k), v)


    def test_delete_client(self):
        '''
        Test deleting a client successful.
        '''
        self.client.force_authenticate(self.sales_employee)

        client = create_client()
        
        url = detail_url(client.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(id=client.id).exists())
