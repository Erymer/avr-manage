"""
Test for inventory APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import EquipmentType

from inventory.serializers import EquipmentTypeSerializer

EQUIPMENT_TYPE_URL = reverse('inventory:equipmenttype-list')

def detail_url(equipment_type_id):
    """Create and return a equipment detail URL"""
    return reverse('inventory:equipmenttype-detail', args=[equipment_type_id])


def create_equipment_type(name="speaker"):
    equipment_type = EquipmentType.objects.create(name=name)
    return equipment_type


def create_user(**params):
    '''
    Create and return a new user.
    '''
    return get_user_model().objects.create_user(**params)


# PUBLIC TESTS
class PublicEquipmentTypeAPITests(TestCase):
    """Test unauthenticated API requests"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(EQUIPMENT_TYPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# PRIVATE TESTS
class PrivateEquipmentTypeAPITests(TestCase):
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

        self.inventory_employee = create_user(
            username = "harry_potter",
            first_name = "Harry",
            fathers_name = "Potter",
            mothers_name = "Evans",
            email='harry@example.com', 
            password='test123',
            role='inventory',
        )


    def test_retrieve_equipment_type(self):
        '''
        Test retrieving a list of equipment types
        '''

        create_equipment_type()

        self.client.force_authenticate(self.tech_employee)

        res = self.client.get(EQUIPMENT_TYPE_URL)

        equipment_type = EquipmentType.objects.all().order_by('-id')
        serializer = EquipmentTypeSerializer(equipment_type, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_create_equipment_type(self):
        '''
        Test creating an equipment type
        '''
        payload = {
            'name': 'microphone',
        }

        # Only inventory employees can have CUD permissions.
        self.client.force_authenticate(self.inventory_employee)

        res = self.client.post(EQUIPMENT_TYPE_URL, payload)


        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        client = EquipmentType.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(client, k), v)


    def test_create_equipment_type_without_permissions(self):
        '''
        Test user creating equipment type without permissions
        '''
        payload = {
            'name': 'microphone',
        }

        self.client.force_authenticate(self.tech_employee)

        res = self.client.post(EQUIPMENT_TYPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    # This model only has one field so is not necessary to test a partial update
    def test_full_update(self):
        '''
        Test full update of an equipment type
        '''
        self.client.force_authenticate(self.inventory_employee)

        equipment_type = create_equipment_type(
            name = "console",
        )

        payload = {
            'name': 'adapter',
        }

        url = detail_url(equipment_type.id)

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        equipment_type.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(equipment_type, k), v)


    def test_delete_client(self):
        '''
        Test deleting a client successful.
        '''
        self.client.force_authenticate(self.inventory_employee)

        equipment_type = create_equipment_type()
        
        url = detail_url(equipment_type.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(EquipmentType.objects.filter(id=equipment_type.id).exists())
