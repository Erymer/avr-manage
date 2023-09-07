"""
Test for event type API.
"""
from django.test import TestCase
from tests.mixin_tests import PublicAPITests, PrivateAPITests
from datetime import datetime
from django.utils import timezone
from rest_framework import status
from django.contrib.auth import get_user_model

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

def date_to_str(data, field_name):
    """
    Helper function to transform a datetime instance into a formatted string

    Parameters
    ----------
    data : Model Instance
        Instance of a model obtained using objects.get() method
    field_name : str
        Model field name of DateTime type.

    Returns
    ------
    string
        Date time in string format %Y-%m-%dT%H:%M:%S

    Raises
    ------
    ValueError
        If specified field is not a DateTime field
    """
    datetime_instance = getattr(data, field_name)
    try:
        formatted_string = datetime_instance.strftime('%Y-%m-%dT%H:%M:%S')
    except AttributeError:
        raise ValueError(f'Model field {field_name} is not a DateTime field')
    return formatted_string


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

        self.customer = Customer.objects.create(
            name="John Doe",
            phone="1234567890",
            email="john@example.com",
            company="Barr Co."
        )

        self.default_model_data = {
            'name': 'Foo Concert',
            'load_in_date': timezone.make_aware(datetime(2023, 7, 18, 13, 0)),
            'load_out_date': timezone.make_aware(datetime(2023, 7, 20, 13, 0)),
            'start_date': timezone.make_aware(datetime(2023, 7, 18, 13, 0)),
            'end_date': timezone.make_aware(datetime(2023, 7, 18, 13, 0)),
            'venue': self.venue,
            'customer': self.customer,
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


    def _create_data(self, **params):
        """
        Extended version of _create_data method.
        Adding "set" statements
        """
        data = super()._create_data(**params)
        data.equipment.set(self.equipment_list)
        data.crew.set(self.crew_list)

        return data


    def test_retrieve_event_instace(self):
        """
        Test retrieving model data.
        """

        data = self.model_class.objects.create(**self.default_model_data)
        data.equipment.set(self.equipment_list)
        data.crew.set(self.crew_list)
        res = self._http_request("get", "tech")

        data = self.model_class.objects.all().order_by('-id')

        serializer = self.serializer(data, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)



    def test_create_event(self):
        '''
        Test creating new event instance
        '''

        payload = {
            'name': 'Foo Concert',
            'load_in_date': "2023-01-01T08:30:00",
            'load_out_date': "2023-01-03T09:30:00",
            'start_date': "2023-01-02T08:00:00",
            'end_date': "2023-01-02T14:30:00",
            'venue': {
                'id': self.venue.id,
            },
            'equipment': [
                {'uid': self.equipment_one.uid},
                {'uid': self.equipment_two.uid},
            ],
            'customer': {
                'id': self.customer.id,
            },
            'crew': [
                {'username': self.inventory_employee.username},
                {'username': self.finance_employee.username},
            ],
            'leader': {
                'username': self.tech_employee.username,
            },
            'comment': "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        }

        res = self._http_request(
            request_type="post", 
            role="sales", 
            payload=payload
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data = self.model_class.objects.get(id=res.data['id'])

        db_serializer = self.serializer(data)
        self.assertEqual(db_serializer.data, res.data)

        # TODO: A way to simplify this maybe?
        self.assertEqual(getattr(data, 'name'), payload['name'])
        self.assertEqual(getattr(data, 'comment'), payload['comment'])
        self.assertEqual(getattr(data, 'venue').id, payload['venue']['id'])
        self.assertEqual(getattr(data, 'customer').id, payload['customer']['id'])
        self.assertEqual(getattr(data, 'leader').username, payload['leader']['username'])

        date_fields = ['load_in_date', 'load_out_date', 'start_date', 'end_date']
        for date_field in date_fields:
            self.assertEqual(date_to_str(data, date_field), payload[date_field])

        equipment_objects = [Equipment.objects.get(uid=e['uid']) for e in payload['equipment']]
        crew_objects = [get_user_model().objects.get(username=c['username']) for c in payload['crew']]

        self.assertCountEqual(data.equipment.all(), equipment_objects)
        self.assertCountEqual(data.crew.all(), crew_objects)


    def test_create_event_without_permissions(self):
        '''
        Test creating an event instance without proper user permissions
        '''
        payload = {
            'name': 'Foo Concert',
            'load_in_date': "2023-01-01T08:30:00",
            'load_out_date': "2023-01-03T09:30:00",
            'start_date': "2023-01-02T08:00:00",
            'end_date': "2023-01-02T14:30:00",
            'venue': {
                'id': self.venue.id,
            },
            'equipment': [
                {'uid': self.equipment_one.uid},
                {'uid': self.equipment_two.uid},
            ],
            'customer': {
                'id': self.customer.id,
            },
            'crew': [
                {'username': self.inventory_employee.username},
                {'username': self.finance_employee.username},
            ],
            'leader': {
                'username': self.tech_employee.username,
            },
            'comment': "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        }

        res = self._http_request("post", "tech", payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)



    def test_partial_event_update(self):
        '''Test event instance partial update in a simple field'''
        venue = Venue.objects.create(
            name="National Auditorium",
            address="First Av #500",
            city="Ba Sing Se",
            state="Earth Nation",
        )

        equipment_three = Equipment.objects.create(
            type=self.equipment_type,
            brand=self.equipment_brand,
            model=self.equipment_model,
            number=3,
        )

        equipment_four = Equipment.objects.create(
            type=self.equipment_type,
            brand=self.equipment_brand,
            model=self.equipment_model,
            number=4,
        )

        customer = Customer.objects.create(
            name="Naomi Nagata",
            phone="3356748592",
            email="naomi@example.com",
            company="Foo Inc."
        )

        payload = {
            'name': 'Qux Live',
            'load_in_date': "2023-02-03T11:00:00",
            'load_out_date': "2023-02-05T13:30:00",
            'start_date': "2023-02-04T09:30:00",
            'end_date': "2023-02-04T20:00:00",
            'venue': {
                'id': venue.id,
            },
            'equipment': [
                {'uid': equipment_three.uid},
                {'uid': equipment_four.uid},
            ],
            'customer': {
                'id': customer.id,
            },
            'crew': [
                {'username': self.sales_employee.username},
                {'username': self.admin_employee.username},
            ],
            'leader': {
                'username': self.finance_employee.username,
            },
        }


        unchanged_data = self.default_model_data['comment']

        data = self._create_data()
        url = self._detail_url(data.id)

        res = self._http_request('patch', 'sales', payload, url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data.refresh_from_db()

        self.assertEqual(getattr(data, 'name'), payload['name'])
        self.assertEqual(getattr(data, 'venue').id, payload['venue']['id'])
        self.assertEqual(getattr(data, 'customer').id, payload['customer']['id'])
        self.assertEqual(getattr(data, 'leader').username, payload['leader']['username'])

        date_fields = ['load_in_date', 'load_out_date', 'start_date', 'end_date']
        for date_field in date_fields:
            self.assertEqual(date_to_str(data, date_field), payload[date_field])

        equipment_objects = [Equipment.objects.get(uid=e['uid']) for e in payload['equipment']]
        crew_objects = [get_user_model().objects.get(username=c['username']) for c in payload['crew']]

        self.assertCountEqual(data.equipment.all(), equipment_objects)
        self.assertCountEqual(data.crew.all(), crew_objects)
        self.assertEqual(getattr(data, 'comment'), unchanged_data)


    def test_partial_event_update_nested_field(self):
            '''Test event instance partial update in a nested field'''
            venue = Venue.objects.create(
                name="National Auditorium",
                address="First Av #500",
                city="Ba Sing Se",
                state="Earth Nation",
            )

            customer = Customer.objects.create(
                name="Naomi Nagata",
                phone="3356748592",
                email="naomi@example.com",
                company="Foo Inc."
            )

            payload = {
                'name': 'Qux Live',
                'load_in_date': "2023-02-03T11:00:00",
                'load_out_date': "2023-02-05T13:30:00",
                'start_date': "2023-02-04T09:30:00",
                'end_date': "2023-02-04T20:00:00",
                'venue': {
                    'id': venue.id,
                },
                'customer': {
                    'id': customer.id,
                },
                'crew': [
                    {'username': self.sales_employee.username},
                    {'username': self.admin_employee.username},
                ],
                'leader': {
                    'username': self.finance_employee.username,
                },
                'comment': "Do not go gentle into that good night"
            }


            unchanged_data = self.equipment_list
            data = self._create_data()
            url = self._detail_url(data.id)

            res = self._http_request('patch', 'sales', payload, url)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            data.refresh_from_db()


            self.assertEqual(getattr(data, 'name'), payload['name'])
            self.assertEqual(getattr(data, 'venue').id, payload['venue']['id'])
            self.assertEqual(getattr(data, 'customer').id, payload['customer']['id'])
            self.assertEqual(getattr(data, 'leader').username, payload['leader']['username'])
            self.assertEqual(getattr(data, 'comment'), payload['comment'])

            date_fields = ['load_in_date', 'load_out_date', 'start_date', 'end_date']
            for date_field in date_fields:
                self.assertEqual(date_to_str(data, date_field), payload[date_field])

            crew_objects = [get_user_model().objects.get(username=c['username']) for c in payload['crew']]

            self.assertCountEqual(data.equipment.all(), unchanged_data)
            self.assertCountEqual(data.crew.all(), crew_objects)


    def test_full_event_update(self):
        '''Test event instance full update'''

        venue = Venue.objects.create(
            name="National Auditorium",
            address="First Av #500",
            city="Ba Sing Se",
            state="Earth Nation",
        )

        equipment_three = Equipment.objects.create(
            type=self.equipment_type,
            brand=self.equipment_brand,
            model=self.equipment_model,
            number=3,
        )

        equipment_four = Equipment.objects.create(
            type=self.equipment_type,
            brand=self.equipment_brand,
            model=self.equipment_model,
            number=4,
        )

        customer = Customer.objects.create(
            name="Naomi Nagata",
            phone="3356748592",
            email="naomi@example.com",
            company="Foo Inc."
        )

        payload = {
            'name': 'Qux Live',
            'load_in_date': "2023-02-03T11:00:00",
            'load_out_date': "2023-02-05T13:30:00",
            'start_date': "2023-02-04T09:30:00",
            'end_date': "2023-02-04T20:00:00",
            'venue': {
                'id': venue.id,
            },
            'equipment': [
                {'uid': equipment_three.uid},
                {'uid': equipment_four.uid},
            ],
            'customer': {
                'id': customer.id,
            },
            'crew': [
                {'username': self.sales_employee.username},
                {'username': self.admin_employee.username},
            ],
            'leader': {
                'username': self.finance_employee.username,
            },
            'comment': "Do not go gentle into that good night..."
        }

        data = self._create_data()
        url = self._detail_url(data.id)

        res = self._http_request('put', 'sales', payload, url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data.refresh_from_db()

        self.assertEqual(getattr(data, 'name'), payload['name'])
        self.assertEqual(getattr(data, 'venue').id, payload['venue']['id'])
        self.assertEqual(getattr(data, 'customer').id, payload['customer']['id'])
        self.assertEqual(getattr(data, 'leader').username, payload['leader']['username'])
        self.assertEqual(getattr(data, 'comment'), payload['comment'])

        date_fields = ['load_in_date', 'load_out_date', 'start_date', 'end_date']
        for date_field in date_fields:
            self.assertEqual(date_to_str(data, date_field), payload[date_field])

        equipment_objects = [Equipment.objects.get(uid=e['uid']) for e in payload['equipment']]
        crew_objects = [get_user_model().objects.get(username=c['username']) for c in payload['crew']]

        self.assertCountEqual(data.equipment.all(), equipment_objects)
        self.assertCountEqual(data.crew.all(), crew_objects)


    def test_full_event_update_fail(self):
        """
        Test event update fails without proper parameters
        """
        venue = Venue.objects.create(
            name="National Auditorium",
            address="First Av #500",
            city="Ba Sing Se",
            state="Earth Nation",
        )

        equipment_three = Equipment.objects.create(
            type=self.equipment_type,
            brand=self.equipment_brand,
            model=self.equipment_model,
            number=3,
        )

        equipment_four = Equipment.objects.create(
            type=self.equipment_type,
            brand=self.equipment_brand,
            model=self.equipment_model,
            number=4,
        )

        customer = Customer.objects.create(
            name="Naomi Nagata",
            phone="3356748592",
            email="naomi@example.com",
            company="Foo Inc."
        )

        payload = {
            'hams': 'Qux Live',
            'load_in_date': "2023-02-03T11:00:00",
            'load_out_date': "2023-02-05T13:30:00",
            'start_date': "2023-02-04T09:30:00",
            'end_date': "2023-02-04T20:00:00",
            'venue': {
                'id': venue.id,
            },
            'equipment': [
                {'uid': equipment_three.uid},
                {'uid': equipment_four.uid},
            ],
            'customer': {
                'id': customer.id,
            },
            'crew': [
                {'username': self.sales_employee.username},
                {'username': self.admin_employee.username},
            ],
            'leader': {
                'username': self.finance_employee.username,
            },
            'barr': "Do not go gentle into that good night..."
        }


        data = self._create_data()
        url = self._detail_url(data.id)
        res = self._http_request('put', 'sales', payload, url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_event(self):
        """
        Test deleting event instance successfully.
        """

        self.deleteModelData('sales')
