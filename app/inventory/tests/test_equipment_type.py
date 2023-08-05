"""
Test for equipment type API.
"""
from django.test import TestCase
from tests.mixin_tests import PublicAPITests, PrivateAPITests

from core.models import EquipmentType
from inventory.serializers import EquipmentTypeSerializer


class PublicEquipmentTypeAPITests(PublicAPITests, TestCase):
    data_url = 'inventory:equipmenttype-list'

    def test_auth_required(self):
        '''Test auth is required to call API'''
        self.authRequired()
        

class PrivateEquipmentTypeAPITests(PrivateAPITests, TestCase):
    """Test authenticated API requests"""
    model_class = EquipmentType
    data_url = 'inventory:equipmenttype-list'
    data_detail_url = 'inventory:equipmenttype-detail'
    serializer = EquipmentTypeSerializer
    default_model_data = {
        'name': 'speaker',
    }


    def test_retrieve_equipment_type(self):
        '''Test retrieving equipment types'''
        self.retrieveModelData(role="tech")


    def test_create_equipment_type(self):
        '''Test creating an equipment type'''
        payload = {
            'name': 'microphone',
        }
        self.createModelData(payload, role="inventory")


    def test_create_equipment_type_without_permissions(self):
        '''Test user creating an equipment type without permissions.'''
        payload = {
            'name': 'microphone',
        }
        self.createModelDataWithoutPermissions(payload, role="tech")


    # EquipmentType model only has one field, so is not necesary to test for
    # partial updates
    def test_full_equipment_type_update(self):
        '''Test full update of a equipment type'''
        payload = {
            'name': 'console',
        }
        self.fullModelDataUpdate(payload, role="inventory")


    def test_delete_client(self):
        '''
        Test delete equipment type successful
        '''
        self.deleteModelData(role="inventory")
