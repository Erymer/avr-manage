"""
Test for event photo API.
"""
from django.test import TestCase, RequestFactory
from tests.mixin_tests import PublicAPITests, PrivateAPITests

from core.models import (
    EventPhoto,
    Venue,
    EquipmentType,
    EquipmentModel,
    EquipmentBrand,
    Equipment,
    Customer,
    Event,
 )

from event.serializers import EventPhotoSerializer
from rest_framework import status

from datetime import datetime
from django.utils import timezone

import tempfile
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

class PublicEventPhotoAPITests(PublicAPITests, TestCase):
    data_url = 'event:eventphoto-list'

    def test_auth_required(self):
        '''Test auth is required to call API'''
        self.authRequired()
        

class PrivatEventPhotoAPITests(PrivateAPITests, TestCase):
    """Test authenticated API requests"""
    model_class = EventPhoto
    data_url = 'event:eventphoto-list'
    data_detail_url = 'event:eventphoto-detail'
    serializer = EventPhotoSerializer

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

        self.customer = Customer.objects.create(
            name="John Doe",
            phone="1234567890",
            email="john@example.com",
            company="Barr Co."
        )

        self.event = Event.objects.create(
            name = 'Foo Concert',
            load_in_date = timezone.make_aware(datetime(2023, 7, 18, 13, 0)),
            load_out_date = timezone.make_aware(datetime(2023, 7, 20, 13, 0)),
            start_date = timezone.make_aware(datetime(2023, 7, 18, 13, 0)),
            end_date = timezone.make_aware(datetime(2023, 7, 18, 13, 0)),
            venue = self.venue,
            customer = self.customer,
            leader = self.tech_employee,
            comment = "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        )

        self.equipment_list = [
                self.equipment_one,
                self.equipment_two,
        ]

        self.crew_list = [
            self.inventory_employee,
            self.finance_employee,
        ]

        self.factory = RequestFactory()


        self.tmpfile = tempfile.NamedTemporaryFile(suffix='.jpg')
        image = Image.new("RGB", (200, 200), "white")
        image.save(self.tmpfile.name, format='JPEG')
        self.default_model_data = {
            'event': self.event,
            'photo': self.tmpfile.name,
        }


    def tearDown(self) -> None:
        os.remove(self.tmpfile.name)

    # def test_upload_image(self):
    #     with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
    #         img = Image.new('RGB', (10, 10))
    #         img.save(image_file, format='JPEG')
    #         image_file.seek(0)
    #         payload = {
    #             'photo': image_file,
    #             'event': self.event.id,
    #         }
    #         self.client.force_authenticate(self.sales_employee)
    #         res = self.client.post(self.data_url, payload, format='multipart')
    #         # print(res.data)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     # self.assertIn('photo', res.data)




    def test_retrieve_event_photo(self):
        '''
        Test retrieving an event photo
        '''
        self._create_data()

        res = self._http_request(request_type="get", role="tech")

        data = self.model_class.objects.all().order_by('-id')

        request = self.factory.get('/')
        serializer_context = {'request': request}
        serializer = self.serializer(data, many=True, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def _test_create_event_photo_instance(self):
        '''
        Test creating new event photo instance through the API
        '''
        image_data = self.tmpfile.read()
        # base64_image = base64.b64encode(image_data).decode('utf-8')
        image_file = SimpleUploadedFile("test_image.jpg", image_data, content_type="image/jpeg")

        payload = {
            'event': {
                'id': self.event.id,
            },
            'photo': image_file,
        }

        self.client.force_authenticate(self.sales_employee)
        print("autenticated")
        res = self.client.post(
                self.data_url,
                payload, 
        )

        serializer = self.serializer(data=payload)
        serializer.is_valid()
        print(serializer.errors)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # data = self.model_class.objects.get(id=res.data['id'])

        # db_serializer = self.serializer(data)
        # self.assertEqual(db_serializer.data, res.data)

        # # TODO: A way to simplify this maybe?
        # self.assertEqual(getattr(data, 'name'), payload['name'])
        # self.assertEqual(getattr(data, 'comment'), payload['comment'])
        # self.assertEqual(getattr(data, 'venue').id, payload['venue']['id'])
        # self.assertEqual(getattr(data, 'customer').id, payload['customer']['id'])
        # self.assertEqual(getattr(data, 'leader').username, payload['leader']['username'])

        # date_fields = ['load_in_date', 'load_out_date', 'start_date', 'end_date']
        # for date_field in date_fields:
        #     self.assertEqual(date_to_str(data, date_field), payload[date_field])

        # equipment_objects = [Equipment.objects.get(uid=e['uid']) for e in payload['equipment']]
        # crew_objects = [get_user_model().objects.get(username=c['username']) for c in payload['crew']]

        # self.assertCountEqual(data.equipment.all(), equipment_objects)
        # self.assertCountEqual(data.crew.all(), crew_objects)


    def test_delete_event_photo(self):
        """
        Test deleting event photo instance successfully.
        """

        self.deleteModelData('sales')
