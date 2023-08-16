"""
Test for equipment brand API.
"""
from django.test import TestCase
from tests.mixin_tests import PublicAPITests, PrivateAPITests
from django.db.models import Count

from core.models import EquipmentBrand
from inventory.serializers import EquipmentBrandSerializer

from django.urls import reverse
from rest_framework import status


class PublicEquipmentBrandAPITests(PublicAPITests, TestCase):
    data_url = 'inventory:equipmentbrand-list'

    def test_auth_required(self):
        '''Test auth is required to call API'''
        self.authRequired()
        

class PrivateEquipmentBrandAPITests(PrivateAPITests, TestCase):
    """Test authenticated API requests"""
    model_class = EquipmentBrand
    data_url = 'inventory:equipmentbrand-list'
    data_detail_url = 'inventory:equipmentbrand-detail'
    serializer = EquipmentBrandSerializer
    default_model_data = {
        'name': 'shure',
    }


    def test_retrieve_equipment_brand(self):
        '''Test retrieving equipment brands'''
        self.retrieveModelData(role="tech")


    def test_create_equipment_brand(self):
        '''Test creating an equipment brand'''
        payload = {
            'name': 'senheiser',
        }
        self.createModelData(payload, role="inventory")


    def test_creating_brand_that_already_exists(self):
        '''Test trying to create a new brand with the same name'''
        self.createModelDataThatAlreadyExists("inventory")


    def test_create_equipment_brand_without_permissions(self):
        '''Test user creating an equipment brand without permissions.'''
        payload = {
            'name': 'yamaha',
        }
        self.createModelDataWithoutPermissions(payload, role="tech")

    # EquipmentBrand model only has one field, so is not necesary to test for
    # partial updates
    def test_full_equipment_brand_update(self):
        '''Test full update of a equipment brand'''
        payload = {
            'name': 'venue',
        }
        self.fullModelDataUpdate(payload, role="inventory")


    def test_delete_equipment_brand(self):
        '''
        Test delete equipment brand successful
        '''
        self.deleteModelData(role="inventory")
