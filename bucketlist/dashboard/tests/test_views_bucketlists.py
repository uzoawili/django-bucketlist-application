from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from dashboard.forms import BucketListForm


class BucketListsTestCase(TestCase):
    """
    Testcase for the Home/Authentication View.
    """
    fixtures = ['sample_data.json']

    def setUp(self):
        """ operations to be done before every test
        """
        # create a test client:
        self.client = Client()
        # log an existing user in:
        self.client.login(username='uzo', password='tia')

    def test_user_can_view_all_their_bucketlists(self):
        """
        Tests that a user can view all their bucket lists
        after :
        """
        response = self.client.get(
            reverse('dashboard:bucketlists'),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('bucketlists', response.context)
        self.assertEqual(len(response.context['bucketlists']), 4)
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'My Bucket Lists')

    def test_user_can_search_bucketlists(self):
        """
        Tests getting bucketlists with search query string parameter
        """
        response = self.client.get(
            '{}?{}'.format(reverse('dashboard:bucketlists'), 'q=kill'),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('bucketlists', response.context)
        self.assertEqual(len(response.context['bucketlists']), 1)

    def test_user_can_view_create_bucketlist_form(self):
        """
        Tests a user can create bucketlist with valid params.
        """
        response = self.client.get(
            reverse('dashboard:bucketlist_create')
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], BucketListForm)
        self.assertFalse(response.context['form'].is_bound)
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Create Bucket List')

    def test_user_can_create_bucketlist_with_valid_params(self):
        """
        Tests a user can create bucketlist with valid params.
        """
        response = self.client.post(
            reverse('dashboard:bucketlist_create'),
            {'name': 'ABC', 'description': 'xyz'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('bucketlists', response.context)
        self.assertEqual(len(response.context['bucketlists']), 5)
        self.assertIn('Bucket List created, nice!', response.content)

    def test_user_cannot_create_bucketlist_without_name(self):
        """
        Tests a user can create bucketlist with valid params.
        """
        response = self.client.post(
            reverse('dashboard:bucketlist_create'),
            {'name': '', 'description': 'xyz'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], BucketListForm)
        self.assertTrue(response.context['form'].is_bound)

    def test_user_can_view_update_bucketlist_form(self):
        """
        Tests a user can update bucketlist with valid params.
        """
        response = self.client.get(
            reverse('dashboard:bucketlist_update')
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], BucketListForm)
        self.assertTrue(response.context['form'].is_bound)
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Update Bucket List')

    def test_user_can_create_bucketlist_with_valid_params(self):
        """
        Tests a user can create bucketlist with valid params.
        """
        response = self.client.post(
            reverse('dashboard:bucketlist_create'),
            {'name': 'ABC', 'description': 'xyz'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('bucketlists', response.context)
        self.assertEqual(len(response.context['bucketlists']), 5)
        self.assertIn('Bucket List created, nice!', response.content)

    def test_user_cannot_create_bucketlist_without_name(self):
        """
        Tests a user can create bucketlist with valid params.
        """
        response = self.client.post(
            reverse('dashboard:bucketlist_create'),
            {'name': '', 'description': 'xyz'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], BucketListForm)
        self.assertTrue(response.context['form'].is_bound)