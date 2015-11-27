from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from dashboard.models import BucketList
from dashboard.forms import BucketListItemForm
from dashboard.views import BucketListItemCreateView,\
                            BucketListItemUpdateView


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

    def test_user_can_view_all_items_in_a_bucketlist(self):
        """
        Tests that a user can view all the items in a bucket list
        as well as it's details:
        """
        response = self.client.get(
            reverse(
                'dashboard:bucketlist_details',
                kwargs={'pk': 71}
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.context)
        self.assertEqual(len(response.context['items']), 3)
        self.assertIn('bucketlist', response.context)
        self.assertIsInstance(response.context['bucketlist'], BucketList)

    def test_user_cannot_view_items_with_invalid_pk(self):
        """
        Tests that a user cannot view items for an invalid
        bucket list pk provided:
        """
        response = self.client.get(
            reverse(
                'dashboard:bucketlist_details',
                kwargs={'pk': 65}
            ),
        )
        self.assertEqual(response.status_code, 404)

    def test_user_can_view_the_create_bucketlist_item_form(self):
        """
        Tests a user can view the create bucketlist item form.
        """
        response = self.client.get(
            reverse('dashboard:bucketlist_item_create', kwargs={'pk': 71})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], BucketListItemForm)
        self.assertFalse(response.context['form'].is_bound)
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Add New Item')

    def test_user_can_create_bucketlist_item_with_valid_params(self):
        """
        Tests a user can create a bucketlist item with valid params.
        """
        response = self.client.post(
            reverse('dashboard:bucketlist_item_create', kwargs={'pk': 71}),
            {'name': 'ABC', 'description': 'xyz'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.context)
        self.assertEqual(len(response.context['items']), 4)
        self.assertIn('Item added to bucket list!', response.content)

    def test_user_cannot_create_item_with_invalid_bucketlist_pk(self):
        """
        Tests a user cannot create a bucketlist without providing
        a name for in the form.
        """
        response = self.client.post(
            reverse('dashboard:bucketlist_item_create', kwargs={'pk': 56}),
            {'name': 'ABC', 'description': 'xyz'},
            follow=True
        )
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_create_bucketlist_item_without_name(self):
        """
        Tests a user cannot create a bucketlist item without providing
        a name in the form.
        """
        response = self.client.post(
            reverse('dashboard:bucketlist_item_create', kwargs={'pk': 71}),
            {'name': '', 'description': 'xyz'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], BucketListItemForm)
        self.assertTrue(response.context['form'].is_bound)
        self.assertEqual(
            response.resolver_match.func.__name__,
            BucketListItemCreateView.as_view().__name__
        )

    def test_user_can_view_the_update_bucketlist_item_form(self):
        """
        Tests a user can update bucketlist item with valid params.
        """
        response = self.client.get(
            reverse(
                'dashboard:bucketlist_item_update',
                kwargs={'pk': 71, 'item_pk': 13}
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], BucketListItemForm)
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Update Item')

    def test_user_cannot_update_bucketlist_item_with_invalid_pks(self):
        """
        Tests a user cannot update bucketlist item with invalid params.
        """
        response = self.client.get(
            reverse(
                'dashboard:bucketlist_item_update',
                kwargs={'pk': 4, 'item_pk': 100}
            ),
        )
        self.assertEqual(response.status_code, 404)

    def test_user_can_update_bucketlist_item_with_valid_params(self):
        """
        Tests a user can update bucketlist item with valid params.
        """
        response = self.client.post(
            reverse(
                'dashboard:bucketlist_item_update',
                kwargs={'pk': 71, 'item_pk': 13}
            ),
            {'name': 'ABCD', 'description': 'stuvwxyz'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.context)
        self.assertEqual(len(response.context['items']), 3)
        self.assertIn('Item updated, cool!', response.content)

    def test_user_cannot_update_bucketlist_item_without_name(self):
        """
        Tests a user cannot update a bucketlist item without providing
        a name for in the form.
        """
        response = self.client.post(
            reverse(
                'dashboard:bucketlist_item_update',
                kwargs={'pk': 71, 'item_pk': 13}
            ),
            {'name': '', 'description': 'stuvwxyz'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], BucketListItemForm)
        self.assertTrue(response.context['form'].is_bound)
        self.assertEqual(
            response.resolver_match.func.__name__,
            BucketListItemUpdateView.as_view().__name__
        )

    def test_user_can_set_bucketlist_item_done_with_valid_params(self):
        """
        Tests a user can update bucketlist item with valid params.
        """
        response = self.client.post(
            reverse(
                'dashboard:bucketlist_item_done',
                kwargs={'pk': 71, 'item_pk': 13}
            ),
            {'done': ''},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.context)
        self.assertEqual(len(response.context['items']), 3)
        self.assertIn('Item marked as done, keep it up!', response.content)

    def test_user_cannot_set_bucketlist_item_done_with_invalid_params(self):
        """
        Tests a user cannot update a bucketlist item with invalid params.
        """
        response = self.client.post(
            reverse(
                'dashboard:bucketlist_item_done',
                kwargs={'pk': 71, 'item_pk': 13}
            ),
            {'name': '', 'description': ''},
            follow=True
        )
        self.assertEqual(response.status_code, 404)

    def test_user_can_view_the_delete_bucketlist_item_form(self):
        """
        Tests a user can delete bucketlist items with valid params.
        """
        response = self.client.get(
            reverse(
                'dashboard:bucketlist_item_delete',
                kwargs={'pk': 71, 'item_pk': 13}
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Delete Item')

    def test_user_cannot_view_delete_bucketlist_item_with_invalid_params(self):
        """
        Tests a user cannot delete bucketlist item with invalid pk or item_pk.
        """
        response = self.client.get(
            reverse(
                'dashboard:bucketlist_item_delete',
                kwargs={'pk': 1, 'item_pk': 8}
            ),
        )
        self.assertEqual(response.status_code, 404)

    def test_user_can_delete_bucketlist_with_valid_params(self):
        """
        Tests a user can delete bucketlist item with valid params.
        """
        response = self.client.post(
            reverse(
                'dashboard:bucketlist_item_delete',
                kwargs={'pk': 71, 'item_pk': 13}
            ),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.context)
        self.assertEqual(len(response.context['items']), 2)
        self.assertIn('Item discarded!', response.content)
