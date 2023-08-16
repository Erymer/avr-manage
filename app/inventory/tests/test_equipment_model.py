"""
Test for equipment model API.
"""
from django.test import TestCase
from tests.mixin_tests import PublicAPITests, PrivateAPITests

from core.models import EquipmentModel
from inventory.serializers import EquipmentModelSerializer


class PublicEquipmentModelAPITests(PublicAPITests, TestCase):
    data_url = 'inventory:equipmentmodel-list'

    def test_auth_required(self):
        '''Test auth is required to call API'''
        self.authRequired()
        

class PrivateEquipmentModelAPITests(PrivateAPITests, TestCase):
    """Test authenticated API requests"""
    model_class = EquipmentModel
    data_url = 'inventory:equipmentmodel-list'
    data_detail_url = 'inventory:equipmentmodel-detail'
    serializer = EquipmentModelSerializer
    default_model_data = {
        'name': 'speaker',
    }


    def test_retrieve_equipment_model(self):
        '''Test retrieving equipment models'''
        self.retrieveModelData(role="tech")


    def test_create_equipment_model(self):
        '''Test creating an equipment model'''
        payload = {
            'name': 'QLXD4',
        }
        self.createModelData(payload, role="inventory")


    def test_create_model_that_already_exists(self):
        '''Test creating a equipment model that already exists'''
        self.createModelDataThatAlreadyExists('inventory')


    def test_create_equipment_model_without_permissions(self):
        '''Test user creating an equipment model without permissions.'''
        payload = {
            'name': 'EMX5000',
        }
        self.createModelDataWithoutPermissions(payload, role="tech")


    # EquipmentModel model only has one field, so is not necesary to test for
    # partial updates
    def test_full_equipment_model_update(self):
        '''Test full update of a equipment model'''
        payload = {
            'name': 'EW100',
        }
        self.fullModelDataUpdate(payload, role="inventory")


    def test_delete_equipment_model(self):
        '''
        Test delete equipment model successful
        '''
        self.deleteModelData(role="inventory")
