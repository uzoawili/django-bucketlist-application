from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class BucketlistsItemsTestCase(APITestCase):
    """ Testcase for the BucketlistItem related API endpoints
    """
    fixtures = ['sample_data.json']

    def setUp(self):
        """ Operations to run before every test
        """
        # log a user in and set authentication token:
        response = self.client.post(
            reverse('api:auth_login'),
            {'username': 'uzo', 'password': 'tia', }
        )
        self.set_request_headers(response.data.get('token'))
        self.user_data = response.data.get('user')

    def set_request_headers(self, token=''):
        """
        Formats the headers to be used when accessing API endpoints.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {}'.format(token)
        )

    def test_create_bucketlist_item_with_name(self):
        """ Tests the create_bucketlist_item API endpoint.
            POST '/bucketlists/<pk>/items/'
        """
        response = self.client.post(
            reverse('api:bucketlist_item_create', kwargs={'pk': 71}),
            {'name': 'ABC', 'done': False, }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('name'), "ABC")
        self.assertEqual(response.data.get('done'), False)

    def test_create_bucketlist_item_without_name(self):
        """ Tests that the create_bucketlist_item API endpoint
            without providing a name errors out.
            POST '/bucketlists/<int:id>/items/'
        """
        response = self.client.post(
            reverse('api:bucketlist_item_create', kwargs={'pk': 71}),
            {'done': False, }
        )
        self.assertEqual(response.status_code, 400)

    def test_create_bucketlist_item_with_invalid_pk(self):
        """ Tests that the create_bucketlist_item API endpoint
            with invalid id errors out.
            POST '/bucketlists/<pk>/items/'
        """
        response = self.client.post(
            reverse('api:bucketlist_item_create', kwargs={'pk': 1}),
            {'name': 'ABC', 'done': False, }
        )
        self.assertEqual(response.status_code, 404)

    def test_update_bucketlist_item_with_valid_pk_and_item_pk(self):
        """ Tests the update bucketlist item when provided
            valid pk and item_pk.
            PUT '/bucketlists/<pk>/items/<iitem_pk>'
        """
        response = self.client.put(
            reverse(
                'api:bucketlist_item_detail',
                kwargs={'pk': 71, 'item_pk': 13}
            ),
            {'name': 'ABCDE', 'done': True, }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('name'), 'ABCDE')
        self.assertEqual(response.data.get('done'), True)

    def test_update_bucketlist_item_with_invalid_pk(self):
        """ Tests that the update bucketlist item
            errors out when provided an invalid pk.
            PUT '/bucketlists/<pk>/items/<item_pk>'
        """
        response = self.client.put(
            reverse(
                'api:bucketlist_item_detail',
                kwargs={'pk': 1, 'item_pk': 13}
            ),
            {'name': 'ABCDE', 'done': True, }
        )
        self.assertEqual(response.status_code, 404)

    def test_update_bucketlist_item_with_invalid_item_pk(self):
        """ Tests that the update bucketlist item
            errors out when provided an invalid item_pk.
            PUT '/bucketlists/<pk>/items/<item_pk>'
        """
        response = self.client.put(
            reverse(
                'api:bucketlist_item_detail',
                kwargs={'pk': 71, 'item_pk': 100}
            ),
            {'name': 'ABCDE', 'done': True, }
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_bucketlist_item_with_valid_pk_and_item_pk(self):
        """ Tests the delete bucketlist_item when provided valid id.
            DELETE '/bucketlists/<pk>/items/<item_pk>'
        """
        response = self.client.delete(
            reverse(
                'api:bucketlist_item_detail',
                kwargs={'pk': 71, 'item_pk': 13}
            ),
        )
        self.assertEqual(response.status_code, 204)
