from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from dashboard.forms import BucketListForm
from dashboard.views import BucketListCreateView,\
                            BucketListUpdateView


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
        Tests that a user can view the create bucketlist form.
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
        Tests a user cannot create a bucketlist without providing
        a name for in the form.
        """
        response = self.client.post(
            reverse('dashboard:bucketlist_create'),
            {'name': '', 'description': 'xyz'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], BucketListForm)
        self.assertTrue(response.context['form'].is_bound)
        self.assertEqual(
            response.resolver_match.func.__name__,
            BucketListCreateView.as_view().__name__
        )

    def test_user_can_view_update_bucketlist_form(self):
        """
        Tests a user can view the update bucketlist form.
        """
        response = self.client.get(
            reverse('dashboard:bucketlist_update', kwargs={'pk': 71}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], BucketListForm)
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Update Bucket List')

    def test_user_cannot_view_update_bucketlist_form_with_invalid_pk(self):
        """
        Tests a user cannot update bucketlist with invalid pk.
        """
        response = self.client.get(
            reverse('dashboard:bucketlist_update', kwargs={'pk': 65}),
        )
        self.assertEqual(response.status_code, 404)

    def test_user_can_update_bucketlist_with_valid_params(self):
        """
        Tests a user can update bucketlist with valid params.
        """
        response = self.client.post(
            reverse('dashboard:bucketlist_update', kwargs={'pk': 71}),
            {'name': 'ABCD', 'description': 'stuvwxyz'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('bucketlists', response.context)
        self.assertEqual(len(response.context['bucketlists']), 4)
        self.assertIn('Bucket List updated, cool!', response.content)

    def test_user_cannot_update_bucketlist_without_name(self):
        """
        Tests a user cannot update a bucketlist without providing
        a name for in the form.
        """
        response = self.client.post(
            reverse('dashboard:bucketlist_update', kwargs={'pk': 71}),
            {'name': '', 'description': 'stuvwxyz'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], BucketListForm)
        self.assertTrue(response.context['form'].is_bound)
        self.assertEqual(
            response.resolver_match.func.__name__,
            BucketListUpdateView.as_view().__name__
        )

    def test_user_can_view_delete_bucketlist_form(self):
        """
        Tests a user can delete bucketlist with valid params.
        """
        response = self.client.get(
            reverse('dashboard:bucketlist_delete', kwargs={'pk': 71}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Delete Bucket List')

    def test_user_cannot_view_delete_bucketlist_form_with_invalid_pk(self):
        """
        Tests a user cannot delete bucketlist with invalid pk.
        """
        response = self.client.get(
            reverse('dashboard:bucketlist_delete', kwargs={'pk': 65}),
        )
        self.assertEqual(response.status_code, 404)

    def test_user_can_delete_bucketlist_with_valid_params(self):
        """
        Tests a user can delete bucketlist with valid params.
        """
        response = self.client.post(
            reverse('dashboard:bucketlist_delete', kwargs={'pk': 71}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('bucketlists', response.context)
        self.assertEqual(len(response.context['bucketlists']), 3)
        self.assertIn('Bucket List discarded!', response.content)
