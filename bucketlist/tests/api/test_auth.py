from rest_framework.test import APITestCase
from rest_framework.reverse import reverse


class AuthenticationTestCase(APITestCase):

    """Testcase for the Authentication related API endpoints.
    """
    fixtures = ['sample_data.json']

    def setUp(self):
        """ Operations to run before every test
        """
        pass

    def test_user_can_register_with_username_and_password(self):
        """
            Tests user registration specifying username and password.
            POST '/auth/register'
        """
        response = self.client.post(
            reverse('api:auth_register'),
            {'username': 'janedoe', 'password': 'something', }
        )
        user = response.data.get('user')
        token = response.data.get('token')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(user.get('username'), 'janedoe')
        self.assertIsNotNone(token)

    def test_register_user_with_existing_username_forbidden(self):
        """ Tests user registration with existing email forbidden.
            POST '/auth/register'
        """
        response = self.client.post(
            reverse('api:auth_register'),
            {'username': 'andela', 'password': 'something', }
        )
        self.assertEqual(response.status_code, 400)

    def test_register_user_without_username_forbidden(self):
        """ Tests user registration without specifying password.
            POST '/auth/register'
        """
        response = self.client.post(
            reverse('api:auth_register'),
            {'password': 'something', }
        )
        self.assertEqual(response.status_code, 400)

    def test_register_user_without_password_forbidden(self):
        """ Tests user registration without specifying password.
            POST '/auth/register'
        """
        response = self.client.post(
            reverse('api:auth_register'),
            {'username': 'andela', }
        )
        self.assertEqual(response.status_code, 400)

    def test_registered_user_login(self):
        """ Tests user login for registered.
            POST '/auth/login'
        """
        response = self.client.post(
            reverse('api:auth_login'),
            {'username': 'andela', 'password': 'tia', }
        )
        user = response.data.get('user')
        token = response.data.get('token')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.get('username'), 'andela')
        self.assertIn(reverse('api:bucketlists'), user.get('bucketlists_url'))
        self.assertIsNotNone(token)

    def test_unregistered_user_login_forbidden(self):
        """ Tests user login for unregistered is not allowed.
            POST '/auth/login'
        """
        response = self.client.post(
            reverse('api:auth_login'),
            {'username': 'janedoe', 'password': 'tia', }
        )
        self.assertEqual(response.status_code, 400)
