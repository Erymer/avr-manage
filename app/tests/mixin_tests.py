"""
Common tests for API's
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Client


def create_user(**params):
    '''
    Create and return a new user.
    '''
    return get_user_model().objects.create_user(**params)

# PUBLIC TESTS
class PublicAPITests(TestCase):
    """
    Test unauthenticated API requests

    Attributes
    ----------
    data_url : str
        Model list url (foo:foo-list)
    """

    def setUp(self):
        self.client = APIClient()

    def authRequired(self):
        """Test auth is required to call API"""
        res = self.client.get(reverse(self.data_url))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# PRIVATE TESTS
class PrivateAPITests(TestCase):
    """
    Test authenticated API requests

    Attributes
    ----------
    model_class : class
        Model that we wish to test
    data_url : str
        Model list url (foo:foo-list)
    data_detail_url : str
        Url to obtain individual instance urls (foo:foo-detail)
    serializer : class
        Model serializer class
    default_model_data : dict
        Dictionary defining model data that will be used as sample data during
        the tests.
        Each element of the dictionary corresponds to a field in the model.
        Key = model field name, Value = model field data.
    """

    def setUp(self):
        self.client = APIClient()
        self.sales_employee = create_user(
            username = "john_doe",
            first_name = "John",
            fathers_name = "Doe",
            mothers_name = "Foo",
            email='john@example.com', 
            password='test123',
            role='sales',
        )

        self.tech_employee = create_user(
            username = "foo_barr",
            first_name = "Foo",
            fathers_name = "Barr",
            mothers_name = "Qux",
            email='foo@example.com', 
            password='test123',
            role='tech',
        )

        self.finance_employee = create_user(
            username = "jack_smith",
            first_name = "Jack",
            fathers_name = "Smith",
            mothers_name = "Don",
            email='jack@example.com', 
            password='test123',
            role='finance',
        )

        self.admin_employee = create_user(
            username = "tosin_abasi",
            first_name = "Tosin",
            fathers_name = "Abasi",
            mothers_name = "Nando",
            email='tosin@example.com', 
            password='test123',
            role='admin',
        )

        self.inventory_employee = create_user(
            username = "harry_potter",
            first_name = "Harry",
            fathers_name = "Potter",
            mothers_name = "Evans",
            email='harry@example.com', 
            password='test123',
            role='inventory',
        )


    def _create_data(self, **params):
        """
        Helper function to create sample model data directly into the data base
        without using the API. Bypasses authentication.
        The data is defined in `default_model_data` when creating the Test
        Class.

        Parameters
        ----------
        **params : dict, optional
            Model data that will be used to create sample data
            Each element of the dictionary corresponds to a field in the model.
            Key = model field name, Value = model field data.
        """
        self.default_model_data.update(params)

        data = self.model_class.objects.create(**self.default_model_data)
        return data


    def _detail_url(self, data_id):
        """
        Helper function to obtain the url of a model instance

        Parameters
        ----------
        data_id : int
            Model instance id
        """
        return reverse(self.data_detail_url, args=[data_id])


    def _rol_selection(self, role):
        """
        Helper function to select employee type to be authenticated
        Parameters
        ----------
        role : String
            Employee role that will be used for the authentication in the test.
            Available roles are: tech, sales, finance, admin, inventory

        Raises
        ------
        ValueError
            If selected role doesn't exists.
        """
        if role.lower() == "tech":
            return self.tech_employee
        elif role.lower() == "sales":
            return self.sales_employee
        elif role.lower() == "finance":
            return self.finance_employee
        elif role.lower() == "admin":
            return self.admin_employee
        elif role.lower() == "inventory":
            return self.inventory_employee
        else:
            raise ValueError("Unavailable role")


    def retrieveModelData(self, role):
        """
        Test retrieving model data.

        Parameters
        ----------
        role : String
            Employee role that will be used for the authentication in the test.
            Available roles are: tech, sales, finance, admin, inventory

        Raises
        ------
        AssertionError
            If data cannot be retrieved or if data in the database differs from
            the data in the default_model_data attribute
        """
        self._create_data()

        employee_role = self._rol_selection(role)
        self.client.force_authenticate(employee_role)

        res = self.client.get(reverse(self.data_url))

        foo = self.model_class.objects.all().order_by('-id')
        serializer = self.serializer(foo, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def createModelData(self, payload, role):
        """
        Test creating model data

        Parameters
        ----------
        payload : dict
            Each element of the dictionary corresponds to a field in the model.
            Key = model field name, Value = model field data.
        role : str
            Employee role that will be used for the authentication in the test.
            Available roles are: tech, sales, finance, admin, inventory

        Raises
        ------
        AssertionError
            If data was not successfully created or if the data in the database
            differs from the data given in the payload.
        """
        employee_role = self._rol_selection(role)
        self.client.force_authenticate(employee_role)

        res = self.client.post(reverse(self.data_url), payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        client = self.model_class.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(client, k), v)


    def createModelDataWithoutPermissions(self, payload, role):
        """
        Test user creating data without proper premissions

        Parameters
        ----------
        payload : dict
            Each element of the dictionary corresponds to a field in the model.
            Key = model field name, Value = model field data.
        role : str
            Employee role that will be used for the authentication in the test.
            Available roles are: tech, sales, finance, admin, inventory

        Raises
        ------
        AssertionError
            If response status code doesn't corresponds to HTTP 403 Forbidden
        """
        employee_role = self._rol_selection(role)
        self.client.force_authenticate(employee_role)

        res = self.client.post(reverse(self.data_url), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    def partialModelDataUpdate(self, original_data_field, payload, role):
        """
        Test partial update of a model data

        Parameters
        ----------
        original_data_field : str
            Name of a field in the model in wich data won't be modified during
            the test. 
        payload : dict
            Data of the model that will be updated.
            This dictionary should not contain data defined in the
            `original_data_field` parameter.
            Each element of the dictionary corresponds to a field in the model.
            Key = model field name, Value = model field data.
        role : str
            Employee role that will be used for the authentication in the test.
            Available roles are: tech, sales, finance, admin, inventory

        Raises
        ------
        AssertionError
            If data was not successfully created, if data in the data base
            differs from the data given in the payload or if the data in the
            field defined in `original_data_field` changed during the test.
        """
        employee_role = self._rol_selection(role)
        self.client.force_authenticate(employee_role)

        original_data = self.default_model_data[original_data_field]

        data = self._create_data()

        url = self._detail_url(data.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data.refresh_from_db()

        for k, v in payload.items():
            self.assertEqual(getattr(data, k), v)
        self.assertEqual(getattr(data, original_data_field), original_data)


    def fullModelDataUpdate(self, payload, role):
        """
        Test full update of model data.

        Parameters
        ----------
        payload : dict
            Data of the model that will be updated.
            Each element of the dictionary corresponds to a field in the model.
            Key = model field name, Value = model field data.
        role : str
            Employee role that will be used for the authentication in the test.
            Available roles are: tech, sales, finance, admin, inventory

        Raises
        ------
        AssertionError
            If data was not successfully created, or if data in the data base
            differs from the data given in the payload.
        """
        employee_role = self._rol_selection(role)
        self.client.force_authenticate(employee_role)

        data = self._create_data()

        url = self._detail_url(data.id)

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(data, k), v)


    def deleteModelData(self, role):
        """
        Test deleting model data successfully.

        Parameters
        ----------
        role : str
            Employee role that will be used for the authentication in the test.
            Available roles are: tech, sales, finance, admin, inventory

        Raises
        ------
        AssertionError
            If data response status code is not HTTP 204 NO CONTENT or if data
            still exists in the data base.
        """
        employee_role = self._rol_selection(role)
        self.client.force_authenticate(employee_role)

        data = self._create_data()
        
        url = self._detail_url(data.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(id=data.id).exists())
