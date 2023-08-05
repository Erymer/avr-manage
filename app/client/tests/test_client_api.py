"""
Test for venue APIs.
"""
from django.test import TestCase
from tests.mixin_tests import PublicAPITests, PrivateAPITests

from core.models import Client
from client.serializers import ClientSerializer


class PublicClientAPITests(PublicAPITests, TestCase):
    data_url = 'client:client-list'
    def test_auth_required(self):
        '''Test auth is required to call API'''
        self.authRequired()
        

class PrivateVenueAPITests(PrivateAPITests, TestCase):
    """Test authenticated API requests"""
    model_class = Client
    data_url = 'client:client-list'
    data_detail_url = 'client:client-detail'
    serializer = ClientSerializer
    default_model_data = {
        'name': 'Legolas Greenleaf',
        'phone': '5645651356',
        'email': 'legolas@example.com',
    }


    def test_retrieve_client(self):
        '''Test retrieving clients'''
        self.retrieveModelData(role="tech")


    def test_create_client(self):
        '''Test creating a client'''
        payload = {
            'name': 'Aragorn Elessar',
            'phone': '3345265845',
            'email': 'aragorn@example.com',
        }
        self.createModelData(payload, role="sales")


    def test_create_client_without_permissions(self):
        '''Test user creating a client without permissions.'''
        payload = {
            'name': 'Faramir Denethor',
            'phone': '7745645315',
            'email': 'faramir@example.com',
        }
        self.createModelDataWithoutPermissions(payload, role="tech")


    def test_full_venue_update(self):
        '''Test full update of a venue'''
        payload = {
            'name': "Boromir Denethor",
            'phone': "6645132568",
            'email': "boromir@example.com",
        }
        self.fullModelDataUpdate(payload, role="sales")

        payload = {
            'name': 'Gimli Gloinson',
            'phone': '4456125865',
            'email': 'gimli@example.com',
        }


    def test_partial_update(self):
        '''Test partial client update'''
        payload = {
            'phone': "4456728595",
        }
        original_data = 'name'
        self.partialModelDataUpdate(original_data, payload=payload, role="sales")


    def test_delete_client(self):
        '''
        Test delete client successful
        '''
        self.deleteModelData(role="sales")
