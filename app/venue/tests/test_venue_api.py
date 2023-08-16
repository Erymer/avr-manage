"""
Test for venue APIs.
"""
from django.test import TestCase
from tests.mixin_tests import PublicAPITests, PrivateAPITests

from core.models import Venue
from venue.serializers import VenueSerializer


class PublicVenueAPITests(PublicAPITests, TestCase):
    data_url = 'venue:venue-list'
    def test_auth_required(self):
        '''Test auth is required to call API'''
        self.authRequired()
        

class PrivateVenueAPITests(PrivateAPITests, TestCase):
    """Test authenticated API requests"""
    model_class = Venue
    data_url = 'venue:venue-list'
    data_detail_url = 'venue:venue-detail'
    serializer = VenueSerializer
    default_model_data = {
        'name': 'Sample Venue',
        'address': 'Foo 123# Col. Barr',
        'city': 'Sample City',
        'state': 'Qux',
    }


    def test_retrieve_venue(self):
        '''Test retrieving venues'''
        self.retrieveModelData(role="tech")


    def test_create_venue(self):
        '''Test creating a venue'''
        payload = {
            'name': 'Sample Venue',
            'address': 'Foo 123# Col. Barr',
            'city': 'Sample City',
            'state': 'Qux',
        }
        self.createModelData(payload, role="sales")


    def test_create_venue_without_permissions(self):
        '''Test user creating venue without permissions.'''
        payload = {
            'name': 'National Auditorium',
            'address': 'First Av no 573. Col. Grand',
            'city': 'Racoon City',
            'state': 'Ba Sing Se',
        }
        self.createModelDataWithoutPermissions(payload, role="tech")


    def test_full_venue_update(self):
        '''Test full update of a venue'''
        payload = {
            'name': 'National Auditorium',
            'address': 'First Av no 573. Col. Grand',
            'city': 'Racoon City',
            'state': 'Ba Sing Se',
        }
        self.fullModelDataUpdate(payload, role="sales")


    def test_partial_update(self):
        '''Test partial venue update'''
        payload = {
            'address': "742 Evergreen Terrace",
        }
        original_data = 'name'
        self.partialModelDataUpdate(original_data, payload=payload, role="sales")


    def test_delete_venue(self):
        '''
       Test delete venue successful
        '''
        self.deleteModelData(role="sales")
