"""
Test for venue APIs.
"""
from django.test import TestCase
from tests.mixin_tests import PublicAPITests, PrivateAPITests

from core.models import Customer
from customer.serializers import CustomerSerializer


class PublicCustomerAPITests(PublicAPITests, TestCase):
    data_url = 'customer:customer-list'
    def test_auth_required(self):
        '''Test auth is required to call API'''
        self.authRequired()
        

class PrivateVenueAPITests(PrivateAPITests, TestCase):
    """Test authenticated API requests"""
    model_class = Customer
    data_url = 'customer:customer-list'
    data_detail_url = 'customer:customer-detail'
    serializer = CustomerSerializer
    default_model_data = {
        'name': 'Legolas Greenleaf',
        'phone': '5645651356',
        'email': 'legolas@example.com',
        'company': 'Foo Inc.',
    }


    def test_retrieve_customer(self):
        '''Test retrieving customers'''
        self.retrieveModelData(role="tech")


    def test_create_customer(self):
        '''Test creating a customer'''
        payload = {
            'name': 'Aragorn Elessar',
            'phone': '3345265845',
            'email': 'aragorn@example.com',
            'company': 'Barr Corp',
        }
        self.createModelData(payload, role="sales")


    def test_create_customer_without_permissions(self):
        '''Test user creating a customer without permissions.'''
        payload = {
            'name': 'Faramir Denethor',
            'phone': '7745645315',
            'email': 'faramir@example.com',
            'company': 'Lorem',
        }
        self.createModelDataWithoutPermissions(payload, role="tech")


    def test_full_venue_update(self):
        '''Test full update of a venue'''
        payload = {
            'name': "Boromir Denethor",
            'phone': "6645132568",
            'email': "boromir@example.com",
            'company': 'Ipsum SA',
        }
        self.fullModelDataUpdate(payload, role="sales")


    def test_partial_update(self):
        '''Test partial customer update'''
        payload = {
            'phone': "4456728595",
        }
        original_data = 'name'
        self.partialModelDataUpdate(original_data, payload=payload, role="sales")


    def test_delete_customer(self):
        '''
        Test delete customer successful
        '''
        self.deleteModelData(role="sales")
