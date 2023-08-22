"""
Test for equipment type API.
"""
from django.test import TestCase
from tests.mixin_tests import PublicAPITests, PrivateAPITests
from datetime import datetime
from django.utils import timezone

from core.models import (
    Event, 
    EquipmentBrand, 
    EquipmentModel, 
    EquipmentType,
    Equipment, 
    Customer,
    Venue,
)
from event.serializers import EventSerializer


class PublicEventAPITests(PublicAPITests, TestCase):
    data_url = 'event:event-list'

    def test_auth_required(self):
        '''Test auth is required to call API'''
        self.authRequired()
        

class PrivateEventAPITests(PrivateAPITests, TestCase):
    """Test authenticated API requests"""
    model_class = Event
    data_url = 'event:event-list'
    data_detail_url = 'event:event-detail'
    serializer = EventSerializer

    def setUp(self):
        super().setUp()
        self.venue = Venue.objects.create(
            name="Sample Place Name",
            address="Foo #350",
            city="Barr",
            state="Ham",
        )

        self.equipment_type = EquipmentType.objects.create(
            name="microphone",
        )
        self.equipment_brand = EquipmentBrand.objects.create(
            name="shure",
        )
        self.equipment_model = EquipmentModel.objects.create(
            name="qlxd",
        )

        self.equipment_one = Equipment.objects.create(
            type=self.equipment_type,
            brand=self.equipment_brand,
            model=self.equipment_model,
            number=1,
        )

        self.equipment_two = Equipment.objects.create(
            type=self.equipment_type,
            brand=self.equipment_brand,
            model=self.equipment_model,
            number=2,
        )

        self.client = Customer.objects.create(
            name="John Doe",
            phone="1234567890",
            email="john@example.com",
            company="Barr Co."
        )

        # self.default_model_data = {
        #     'name': 'Foo Concert',
        #     'load_in_date': "2023-01-01T08:30:00",
        #     'load_out_date': "2023-01-03T09:30:00",
        #     'start_date': "2023-01-02T08:00:00",
        #     'end_date': "2023-01-02T14:30:00",
        #     'venue': {
        #         'id': self.venue.id,
        #     },
        #     'equipment': [
        #         {'uid': self.equipment_one.uid},
        #         {'uid': self.equipment_two.uid},
        #     ],
        #     'client': {
        #         'id': self.client.id,
        #     },
        #     'crew': [
        #         {'username': self.inventory_employee.username},
        #         {'username': self.finance_employee.username},
        #     ],
        #     'leader': {
        #         'username': self.tech_employee.username,
        #     },
        #     'comment': "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        # }

        self.default_model_data = {
            'name': 'Foo Concert',
            'load_in_date': timezone.make_aware(datetime(2023, 7, 18, 13, 0)),
            'load_out_date': timezone.make_aware(datetime(2023, 7, 20, 13, 0)),
            'start_date': timezone.make_aware(datetime(2023, 7, 18, 13, 0)),
            'end_date': timezone.make_aware(datetime(2023, 7, 18, 13, 0)),
            'venue': self.venue,
            'client': self.client,
            'leader': self.tech_employee,
            'comment': "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        }
        self.equipment_list = [
                self.equipment_one,
                self.equipment_two,
            ]
        self.crew_list = [
            self.inventory_employee,
            self.finance_employee,
        ]


    # def test_retrieve_event(self):
    #     '''Test retrieving equipment types'''
    #     self.retrieveModelData(role="tech")

    # def test_retrieve_event_instace(self):
    #     """
    #     Test retrieving model data.
    #     """

    #     data = self.model_class.objects.create(**self.default_model_data)
    #     data.equipment.set(self.equipment_list)
    #     data.crew.set(self.crew_list)
    #     res = self._http_request("get", "tech")

    #     data = self.model_class.objects.all().order_by('-id')
    #     serializer = self.serializer(data, many=True)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)



    # def test_create_equipment_type(self):
    #     '''Test creating an equipment type'''
    #     payload = {
    #         'name': 'microphone',
    #     }
    #     self.createModelData(payload, role="inventory")


    # def test_create_type_that_already_exists(self):
    #     '''Test creating a type that already exists'''
    #     self.createModelDataThatAlreadyExists('inventory')


    # def test_create_equipment_type_without_permissions(self):
    #     '''Test user creating an equipment type without permissions.'''
    #     payload = {
    #         'name': 'microphone',
    #     }
    #     self.createModelDataWithoutPermissions(payload, role="tech")


    # # EquipmentType model only has one field, so is not necesary to test for
    # # partial updates
    # def test_full_equipment_type_update(self):
    #     '''Test full update of a equipment type'''
    #     payload = {
    #         'name': 'console',
    #     }
    #     self.fullModelDataUpdate(payload, role="inventory")


    # def test_delete_equipment_type(self):
    #     '''
    #     Test delete equipment type successful
    #     '''
    #     self.deleteModelData(role="inventory")
