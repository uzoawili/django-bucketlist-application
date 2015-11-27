from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class HomeViewTestCase(TestCase):
    """
    Testcase for the Home/Authentication View .
    """
    fixtures = ['sample_data.json']

    def setUp(self):
        """ operations to be done before every test
        """
        # create a test client:
        self.client = Client()

    def test_get_home_view_returns_success(self):
        """
        Tests that a get request to the home/index
        view returns and renders successfully.
        """
        response = self.client.get(
            reverse('home')
        )
        self.assertEquals(response.status_code, 200)

    def test_user_signup_with_valid_params(self):
        """
        Tests that a user can signup from the home view:
        """
        response = self.client.post(
            reverse('home'),
            {
                'signup': '',
                'username': 'masterp',
                'password1': 'tia',
                'password2': 'tia'
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_user_cannot_signup_with_existing_username(self):
        """
        Tests that a user cannot signup with the same
        username as an existing user:
        """
        response = self.client.post(
            reverse('home'),
            {
                'signup': '',
                'username': 'uzo',
                'password1': 'tia',
                'password2': 'tia'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid username or password!', response.content)

    def test_user_cannot_signup_without_confirming_password(self):
        """
        Tests that a user cannot signup with the same
        username as an existing user:
        """
        response = self.client.post(
            reverse('home'),
            {
                'signup': '',
                'username': 'uzo',
                'password1': 'tia',
                'password2': 'tis'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid username or password!', response.content)

    def test_user_signin_with_valid_params(self):
        """
        Tests that a registered user can signin from the home view:
        """
        response = self.client.post(
            reverse('home'),
            {
                'signin': '',
                'username': 'uzo',
                'password': 'tia',
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_unregistered_user_cannot_signin(self):
        """
        Tests that an unregistered user cannot
        signin from the home view:
        """
        response = self.client.post(
            reverse('home'),
            {
                'signin': '',
                'username': 'masterp',
                'password': 'tia',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid username or password!', response.content)

    def test_user_logout(self):
        """
        Tests that the user can logout.
        """
        response = self.client.get(
            reverse('signout')
        )
        self.assertEqual(response.status_code, 302)
