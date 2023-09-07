"""
Test for Models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from datetime import datetime
from django.utils import timezone
from unittest.mock import patch

DEFAULT_USERNAME = "john_doe"
DEFAULT_FIRST_NAME = "John"
DEFAULT_FATHERS_NAME = "Doe"
DEFAULT_MOTHERS_NAME = "Foo"
DEFAULT_EMAIL = "jonh@example.com"
DEFAULT_ROLE = "tech"
DEFAULT_PASSWORD = 'testpass123'

# TODO: A way to make this function use less parameters.
def create_employee(username=DEFAULT_USERNAME, first_name=DEFAULT_FIRST_NAME,
                fathers_name=DEFAULT_FATHERS_NAME,
                mothers_name=DEFAULT_MOTHERS_NAME, email=DEFAULT_EMAIL,
                role=DEFAULT_ROLE, password=DEFAULT_PASSWORD):
    '''Create user helper function'''

    employee = get_user_model().objects.create_user(
        username=username,
        first_name=first_name,
        fathers_name=fathers_name,
        mothers_name=mothers_name,
        email=email, role=role,
        password=password,
    )

    return employee


class ModelTest(TestCase):
    """Test models."""

    def test_create_user(self):
        '''
        Test creating a user sucessful
        '''
        user = create_employee()

        self.assertEqual(user.username, DEFAULT_USERNAME)
        self.assertEqual(user.first_name, DEFAULT_FIRST_NAME)
        self.assertEqual(user.fathers_name, DEFAULT_FATHERS_NAME)
        self.assertEqual(user.mothers_name, DEFAULT_MOTHERS_NAME)
        self.assertEqual(user.role, DEFAULT_ROLE)
        self.assertEqual(user.email, DEFAULT_EMAIL)
        self.assertTrue(user.check_password(DEFAULT_PASSWORD))


    def test_normal_user_is_not_superuser(self):
        '''
        Test if a normal user doesn't have super user permissions
        '''
        user = create_employee()
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    
    # TODO: Hacer mas pruebas para verificar validaciones. Por ejemplo, que
    # correo sea correcto, username sin espacios, no se puede crear sin asignar
    # rol etc.

    # def test_new_user_without_email_raises_error(self):
    #     '''
    #     Test that creating a user without an email raises a ValueError.
    #     '''
    #     with self.assertRaises(ValueError):
    #         get_user_model().objects.create_user('', 'test123')


    # def test_new_user_username_normalized(self):
    #     '''
    #     Test username is normalized when creating a user
    #     '''
    #     pass


    # def test_new_user_email_normalized(self):
    #     '''
    #     Test email is normalized for new users
    #     '''
    #     sample_emails = [
    #         ['test1@EXAMPLE.com', 'test1@example.com'],
    #         ['test2@Example.com', 'test2@example.com'],
    #         ['test3@EXAMPLE.COM', 'test3@example.com'],
    #         ['test4@example.COM', 'test4@example.com'],
    #     ]

    #     for email, expected in sample_emails:
    #         user = get_user_model().objects.create_user(email, 'sample123')
    #         self.assertEqual(user.email, expected)


    def test_create_superuser(self):
        '''
        Test creating a superuser
        '''
        user = get_user_model().objects.create_superuser(
            username=DEFAULT_USERNAME,
            first_name=DEFAULT_FIRST_NAME,
            fathers_name=DEFAULT_FATHERS_NAME,
            mothers_name=DEFAULT_MOTHERS_NAME,
            email=DEFAULT_EMAIL, role=DEFAULT_ROLE,
            password=DEFAULT_PASSWORD
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


    # TODO: More unit test for validations. eg: venue name normalized, etc
    def test_create_venue(self):
        '''
        Test Creating a venue is successful
        '''
        venue = models.Venue.objects.create(
            name="Sample Place Name",
            address="Foo #350",
            city="Barr",
            state="Ham",
        )

        saved_venue = models.Venue.objects.get(id=venue.id)

        self.assertEqual(venue, saved_venue)


    # TODO: More unit test for validations:
    def test_create_client(self):
        """Test creating a client is sucessful"""
        client = models.Customer.objects.create(
            name="John Doe",
            phone="1234567890",
            email="john@example.com",
            company="Foo Inc.",
        )

        saved_client = models.Customer.objects.get(id=client.id)

        self.assertEqual(client, saved_client)


    def test_create_equipment_model(self):
        """Test creating an equipment model is sucessful"""
        equipment_model = models.EquipmentModel.objects.create(
            name="QLXD",
        )

        saved_equipment_model = models.EquipmentModel.objects.get(id=equipment_model.id)

        self.assertEqual(equipment_model, saved_equipment_model)


    def test_create_equipment_brand(self):
        """Test creating a equipment_brand is sucessful"""
        equipment_brand = models.EquipmentBrand.objects.create(
            name="Shure",
        )
    
        saved_equipment_brand = models.EquipmentBrand.objects.get(id=equipment_brand.id)
    
        self.assertEqual(equipment_brand, saved_equipment_brand)


    def test_create_equipment_type(self):
        """Test creating a equipment_type is sucessful"""
        equipment_type = models.EquipmentType.objects.create(
            name="Microphone",
        )
    
        saved_equipment_type = models.EquipmentType.objects.get(id=equipment_type.id)
    
        self.assertEqual(equipment_type, saved_equipment_type)


    def test_create_equipment(self):
        """Test creating a equipment is sucessful"""
        equipment_type = models.EquipmentType.objects.create(
            name="Microphone",
        )
        equipment_brand = models.EquipmentBrand.objects.create(
            name="Shure",
        )
        equipment_model = models.EquipmentModel.objects.create(
            name="QLXD",
        )

        equipment = models.Equipment.objects.create(
            type=equipment_type,
            brand=equipment_brand,
            model=equipment_model,
            number=1,
            serial_number="A1234BW2"
        )
    
        saved_equipment = models.Equipment.objects.get(id=equipment.id)
    
        self.assertEqual(equipment, saved_equipment)


    def test_create_equipment_uids(self):
        """Test if each equipment of the same type brand and model has diferent
        uid"""
        equipment_type = models.EquipmentType.objects.create(
            name="Microphone",
        )
        equipment_brand = models.EquipmentBrand.objects.create(
            name="Shure",
        )
        equipment_model = models.EquipmentModel.objects.create(
            name="QLXD",
        )

        equipment_one = models.Equipment.objects.create(
            type=equipment_type,
            brand=equipment_brand,
            model=equipment_model,
            number=1,
        )

        equipment_two = models.Equipment.objects.create(
            type=equipment_type,
            brand=equipment_brand,
            model=equipment_model,
            number=2,
        )
    
        saved_equipment_one = models.Equipment.objects.get(id=equipment_one.id)
        saved_equipment_two = models.Equipment.objects.get(id=equipment_two.id)
    
        self.assertNotEqual(saved_equipment_two.uid, saved_equipment_one.uid)


    def test_create_event(self):
        """Test creating a event is sucessful"""
        user_one = create_employee()
        user_two = create_employee(
            username="jane_doe",
            email="jane@example.com",
        )

        venue = models.Venue.objects.create(
            name="Sample Place Name",
            address="Foo #350",
            city="Barr",
            state="Ham",
        )

        equipment_type = models.EquipmentType.objects.create(
            name="Microphone",
        )
        equipment_brand = models.EquipmentBrand.objects.create(
            name="Shure",
        )
        equipment_model = models.EquipmentModel.objects.create(
            name="QLXD",
        )

        equipment_one = models.Equipment.objects.create(
            type=equipment_type,
            brand=equipment_brand,
            model=equipment_model,
            number=1,
        )

        equipment_two = models.Equipment.objects.create(
            type=equipment_type,
            brand=equipment_brand,
            model=equipment_model,
            number=2,
        )

        customer = models.Customer.objects.create(
            name="John Doe",
            phone="1234567890",
            email="john@example.com",
            company="Foo Barr Co."
        )


        equipment_list = [equipment_one, equipment_two,]
        crew = [user_one, user_two]

        event = models.Event.objects.create(
            name = "John Wedding",
            load_in_date = timezone.make_aware(datetime(2023, 7, 18, 13, 0)),
            load_out_date = timezone.make_aware(datetime(2023, 7, 20, 13, 0)),
            start_date = timezone.make_aware(datetime(2023, 7, 18, 13, 0)),
            end_date = timezone.make_aware(datetime(2023, 7, 18, 13, 0)),
            venue = venue,
            customer = customer,
            leader = user_one,
            comment = "This is just a random comment."
        )

        event.equipment.set(equipment_list)
        event.crew.set(crew)

        saved_event = models.Event.objects.get(id=event.id)
        self.assertEqual(event, saved_event)


    @patch('core.models.uuid.uuid4')
    def test_event_photo_name_uuid(self, mock_uuid):
        '''
        Test generating image path.
        '''
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.event_photo_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/events/photos/{uuid}.jpg')


    @patch('core.models.uuid.uuid4')
    def test_event_file_name_uuid(self, mock_uuid):
        '''
        Test generating file path.
        '''
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.event_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/events/files/{uuid}.jpg')
