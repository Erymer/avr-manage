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
        By default the data is defined in `default_model_data` when creating
        the Test Class.

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


    def _http_request(self, request_type, role, payload=None, url=None):
        '''
        Helper function to create a http requests as a specific user type
        Parameters
        ----------
        request_type : str
            HTTP request type. Possible values are: "post", "get", "put",
            "patch", "delete".
        role : str
            Employee role that will be used for the authentication in the test.
            Available roles are: tech, sales, finance, admin, inventory
        payload : dict
            Payload for the request
        url : str
            Url for the request

        Raises
        ------
        ValueError
            If http request type doesn't exists
        '''
        if url is None:
            url = self.data_url
            url=reverse(url)

        employee_role = self._rol_selection(role)
        self.client.force_authenticate(employee_role)

        if request_type.lower() == 'post':
            res = self.client.post(
                    url, 
                    payload, 
                    format='json'
            )

        elif request_type.lower() == 'get':
            res = self.client.get(
                url, 
            )

        elif request_type.lower() == 'delete':
            res = self.client.delete(
                url, 
            )

        elif request_type.lower() == 'put':
            res = self.client.put(
                url, 
                payload, 
                format='json'
            )

        elif request_type.lower() == 'patch':
            res = self.client.patch(
                url, 
                payload, 
                format='json'
            )

        else:
            raise ValueError(f"{request_type} is an invalid HTTP method")

        return res


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
        res = self._http_request('get', role)
        data = self.model_class.objects.all().order_by('-id')
        serializer = self.serializer(data, many=True)
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
        res = self._http_request('post', role, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data = self.model_class.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(data, k), v)


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
        res = self._http_request('post', role, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    def createModelDataThatAlreadyExists(self, role):
        """
        Test trying to create a new instance with the same data as a previously
        created instance. This test is for models that has one or more fields
        with 'unique=True' parameter.

        Parameters
        ----------
        role : str
            Employee role that will be used for the authentication in the test.
            Available roles are: tech, sales, finance, admin, inventory

        Raises
        ------
        AssertionError
            If response status code doesn't corresponds to HTTP 400 BAD REQUEST
            or if exists more than one instance with the same data
        """
        self._create_data()
        payload = self.default_model_data
        res = self._http_request('post', role, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        count = self.model_class.objects.filter(**payload).count()
        self.assertEqual(count, 1)


    def partialModelDataUpdate(self, original_data_field, payload, role):
        # TODO: Create exception if 'payload' contains 'original_data_field' 
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

        original_data = self.default_model_data[original_data_field]
        data = self._create_data()
        url = self._detail_url(data.id)
        res = self._http_request('patch', role, payload, url)
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

        data = self._create_data()
        url = self._detail_url(data.id)
        res = self._http_request('put', role, payload, url)
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

        data = self._create_data()
        url = self._detail_url(data.id)
        res = self._http_request('delete', role, url=url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.model_class.objects.filter(id=data.id).exists())
