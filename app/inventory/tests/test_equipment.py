"""
Equipment API tests
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from core.models import Equipment, EquipmentModel, EquipmentBrand, EquipmentType
from inventory.serializers import EquipmentSerializer
from tests.mixin_tests import PublicAPITests, PrivateAPITests

from rest_framework import status


class PublicEquipmentAPITests(PublicAPITests, TestCase):
    data_url = 'inventory:equipment-list'
    def test_auth_required(self):
        '''Test auth is required to call API'''
        self.authRequired()


class PrivateEquipmentAPITests(PrivateAPITests, TestCase):
    """
    Test authenticated API requests
    """
    model_class = Equipment
    data_url = 'inventory:equipment-list'
    data_detail_url = 'inventory:equipment-detail'
    serializer = EquipmentSerializer

    def setUp(self):
        super().setUp()
        self.equipment_model = EquipmentModel.objects.create(name="emx500")
        self.equipment_brand = EquipmentBrand.objects.create(name="yamaha")
        self.equipment_type = EquipmentType.objects.create(name="console")
        self.default_model_data = {
            'model': self.equipment_model,
            'brand': self.equipment_brand,
            'type': self.equipment_type,
            'number': 1,
            'serial_number': 'ABC123',
        }


    def test_retrieve_equipment_instace(self):
        """
        Test retrieving model data.
        """

        data = self.model_class.objects.create(**self.default_model_data)
        res = self._http_request("get", "tech")

        data = self.model_class.objects.all().order_by('-id')
        serializer = self.serializer(data, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_create_equipment_with_existing_type_brand_model(self):
        '''
        Test creating equipment instance with previously created 'model',
        'type', 'brand' instances.
        '''
        payload = {
            'model': {
                'name': self.equipment_model.name,
            },
            'type': {
                'name': self.equipment_type.name,
            },
            'brand': {
                'name': self.equipment_brand.name,
            },
            'number': 2,
            'serial_number': "123BCD",
        }
        res = self._http_request("post", "inventory", payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        data = self.model_class.objects.get(id=res.data['id'])

        for key, value in payload.items():
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    self.assertEqual(getattr(data, key).name, nested_value)
            else:
                self.assertEqual(getattr(data, key), value)

        self.assertEqual(self.equipment_model, data.model)
        self.assertEqual(self.equipment_type, data.type)
        self.assertEqual(self.equipment_brand, data.brand)


    def test_create_equipment_with_new_type_brand_model(self):
        '''
        Test creating equipment instance with new 'model', 'type', 'brand'
        instances.
        '''
        payload = {
            'model': {
                'name': 'qlxd',
            },
            'type': {
                'name': 'microphone',
            },
            'brand': {
                'name': 'shure',
            },
            'number': 99,
            'serial_number': "abc123",
        }

        res = self._http_request("post", "inventory", payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        data = self.model_class.objects.get(id=res.data['id'])

        model_exists = EquipmentModel.objects.filter(
            name=payload['model']['name']).exists()
        brand_exists = EquipmentBrand.objects.filter(
            name=payload['brand']['name']).exists()
        type_exists = EquipmentType.objects.filter(
            name=payload['type']['name']).exists()
        self.assertTrue(model_exists)
        self.assertTrue(brand_exists)
        self.assertTrue(type_exists)

        # TODO: Add this loop to createModelData in mixins tests
        for key, value in payload.items():
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    self.assertEqual(getattr(data, key).name, nested_value)
            else:
                self.assertEqual(getattr(data, key), value)


    def test_create_equipment_without_permissions(self):
        '''
        Test creating an equipment instance without proper user permissions
        '''
        payload = {
            'model': {
                'name': self.equipment_model.name,
            },
            'type': {
                'name': self.equipment_type.name,
            },
            'brand': {
                'name': self.equipment_brand.name,
            },
            'number': 3,
            'serial_number': "123BCD",
        }

        res = self._http_request("post", "tech", payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    def test_partial_equipment_update_with_new_brand_type_model(self):
        '''Test equipment instance partial with new model, brand and type'''

        payload = {
            'model': {
                'name': 'cl-5',
            },
            'brand': {
                'name': 'beringher',
            },
            'type': {
                'name': 'desk',
            },
            'serial_number': "123BCD",
        }
        original_data = self.default_model_data['number']

        data = self._create_data()
        url = self._detail_url(data.id)

        res = self._http_request('patch', 'inventory', payload, url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data.refresh_from_db()

        for key, value in payload.items():
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    self.assertEqual(getattr(data, key).name, nested_value)
            else:
                self.assertEqual(getattr(data, key), value)
        self.assertEqual(getattr(data, 'number'), original_data)
        model_exists = EquipmentModel.objects.filter(
            name=payload['model']['name']).exists()
        brand_exists = EquipmentBrand.objects.filter(
            name=payload['brand']['name']).exists()
        type_exists = EquipmentType.objects.filter(
            name=payload['type']['name']).exists()
        self.assertTrue(model_exists)
        self.assertTrue(brand_exists)
        self.assertTrue(type_exists)


    def test_partial_equipment_update(self):
        '''Test equipment instance partial with existing model, brand and type'''
        model = EquipmentModel.objects.create(name="tf5")
        brand = EquipmentBrand.objects.create(name="qux")
        type = EquipmentType.objects.create(name="mixer")

        payload = {
            'model': {
                'name': model.name,
            },
            'brand': {
                'name': brand.name,
            },
            'type': {
                'name': type.name,
            },
            'serial_number': "123BCD",
        }
        original_data = self.default_model_data['number']

        data = self._create_data()
        url = self._detail_url(data.id)

        res = self._http_request('patch', 'inventory', payload, url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data.refresh_from_db()

        for key, value in payload.items():
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    self.assertEqual(getattr(data, key).name, nested_value)
            else:
                self.assertEqual(getattr(data, key), value)
        self.assertEqual(getattr(data, 'number'), original_data)
        self.assertEqual(model, data.model)
        self.assertEqual(type, data.type)
        self.assertEqual(brand, data.brand)



    # def test_partialModelDataUpdateFail(self):
    #     '''
    #     Test equipment instance partial update returns bad request if
    #     parameters are not correct
    #     '''
    #     payload = {
    #         'foo': "123BCD",
    #     }
    #     data = self._create_data()
    #     url = self._detail_url(data.id)
    #     res = self._http_request('patch', 'inventory', payload, url)
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_full_model_update_with_new_type_brand_model(self):
        """
        Test full update of model data creating new type, brand and model
        instances.
        """
        payload = {
            'model': {
                'name': 'sc48',
            },
            'type': {
                'name': 'mixer',
            },
            'brand': {
                'name': 'venue',
            },
            'serial_number': "6845CHBG",
            'number': 15,
        }

        data = self._create_data()
        url = self._detail_url(data.id)
        res = self._http_request('put', 'inventory', payload, url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data.refresh_from_db()
        for key, value in payload.items():
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    self.assertEqual(getattr(data, key).name, nested_value)
            else:
                self.assertEqual(getattr(data, key), value)
        model_exists = EquipmentModel.objects.filter(
            name=payload['model']['name']).exists()
        brand_exists = EquipmentBrand.objects.filter(
            name=payload['brand']['name']).exists()
        type_exists = EquipmentType.objects.filter(
            name=payload['type']['name']).exists()
        self.assertTrue(model_exists)
        self.assertTrue(brand_exists)
        self.assertTrue(type_exists)


    def test_full_equipment_update_with_existing_type_model_brand(self):
        '''Test equipment instance full update with existing model, brand and type'''
        model = EquipmentModel.objects.create(name="tf5")
        brand = EquipmentBrand.objects.create(name="qux")
        type = EquipmentType.objects.create(name="mixer")


        payload = {
            'model': {
                'name': model.name,
            },
            'type': {
                'name': type.name,
            },
            'brand': {
                'name': brand.name,
            },
            'serial_number': "123BCD",
            'number': 10,
        }

        data = self._create_data()
        url = self._detail_url(data.id)

        res = self._http_request('put', 'inventory', payload, url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data.refresh_from_db()

        for key, value in payload.items():
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    self.assertEqual(getattr(data, key).name, nested_value)
            else:
                self.assertEqual(getattr(data, key), value)
        self.assertEqual(model, data.model)
        self.assertEqual(type, data.type)
        self.assertEqual(brand, data.brand)


    def test_fullModelDataUpdateFail(self):
        """
        Test instance update fails without proper parameters
        """
        payload = {
            'model': {
                'name': 'sc48',
            },
            'type': {
                'name': 'mixer',
            },
            'brand': {
                'name': 'venue',
            },
            'barr': 2,
            'serial_number': "6845CHBG",
        }

        data = self._create_data()
        url = self._detail_url(data.id)
        res = self._http_request('put', 'inventory', payload, url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_equipment(self):
        """
        Test deleting equipment instance successfully.
        """

        self.deleteModelData('inventory')
