from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class BucketlistsTestCase(APITestCase):

    """ Testcase for the Bucketlist related API endpoints
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

    def test_get_bucketlists_with_default_parameters(self):
        """ Tests the get_bucketlists API endpoint with no/default
            query string parameters
            GET '/bucketlists/'
        """
        response = self.client.get(
            reverse('api:bucketlists'),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('results')), 4)
        self.assertEqual(response.data.get('count'), 4)
        self.assertEqual(response.data.get('previous'), None)
        self.assertEqual(response.data.get('next'), None)

    def test_get_bucketlists_with_limit_and_page_parameters(self):
        """ Tests the get_bucketlists API endpoint with limit
            and page_parameters query string parameters
            GET '/bucketlists/?limit=1&page=2'
        """
        response = self.client.get(
            '{}?{}'.format(reverse('api:bucketlists'), 'limit=2&page=1'),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('results')), 2)
        self.assertEqual(response.data.get('count'), 4)
        self.assertEqual(response.data.get('previous'), None)
        self.assertIn(
            '{}?{}'.format(reverse('api:bucketlists'), 'limit=2&page=2'),
            response.data.get('next')
        )

    def test_get_bucketlists_with_search_parameter(self):
        """ Tests the get bucketlists API endpoint with serach query string parameters
            GET '/bucketlists/?q=brooklyn'
        """
        response = self.client.get(
            '{}?{}'.format(reverse('api:bucketlists'), 'q=Kill&limit=2')
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertEqual(response.data.get('count'), 1)
        self.assertEqual(response.data.get('previous'), None)
        self.assertEqual(response.data.get('next'), None)

    def test_get_bucketlist_with_valid_id(self):
        """ Tests the get bucketlist API using valid id.
            GET '/bucketlists/71'
        """
        bucketlist_url = reverse('api:bucketlist_detail', kwargs={'pk': 71})
        create_item_url = reverse(
            'api:bucketlist_item_create', kwargs={'pk': 71})
        response = self.client.get(bucketlist_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('name'), "People to Kill")
        self.assertEqual(len(response.data.get('items')), 3)
        self.assertIn(bucketlist_url, response.data.get('url'))
        self.assertIn(create_item_url, response.data.get('create_item_url'))

    def test_get_bucketlist_with_invalid_id(self):
        """ Tests the get_bucketlist API endpoint using invalid id.
            GET '/bucketlists/5'
        """
        bucketlist_url = reverse('api:bucketlist_detail', kwargs={'pk': 5})
        response = self.client.get(bucketlist_url)

        self.assertEqual(response.status_code, 404)

    def test_create_bucketlist_with_name(self):
        """ Tests the create_bucketlist API endpoint
            with a name provided.
            POST '/bucketlists/'
        """
        response = self.client.post(
            reverse('api:bucketlists'),
            {'name': 'ABC', 'description': 'xyz'}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('name'), "ABC")
        self.assertEqual(response.data.get('description'), "xyz")
        self.assertEqual(
            response.data.get('created_by').get('username'),
            self.user_data.get('username')
        )

    def test_create_bucketlist_without_name(self):
        """ Tests that the create_bucketlist API endpoint
            without providing a name errors out.
            POST '/bucketlists/'
        """
        response = self.client.post(
            reverse('api:bucketlists'),
            {'description': 'xyz'}
        )
        self.assertEqual(response.status_code, 400)

    def test_update_bucketlist_with_valid_id(self):
        """ Tests update bucketlist when provided valid id.
            PUT '/bucketlists/71'
        """
        response = self.client.put(
            reverse('api:bucketlist_detail', kwargs={'pk': 71}),
            {'name': 'People to Save', 'description': 'xyz'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('name'), 'People to Save')
        self.assertEqual(response.data.get('description'), "xyz")
        self.assertEqual(
            response.data.get('created_by').get('username'),
            self.user_data.get('username')
        )

    def test_update_bucketlist_with_invalid_id(self):
        """ Tests that update bucketlist errors out
            when provided an invalid id.
            PUT '/bucketlists/1'
        """
        response = self.client.put(
            reverse('api:bucketlist_detail', kwargs={'pk': 1}),
            {'name': 'People to Save', 'description': 'xyz'}
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_bucketlist_with_valid_id(self):
        """ Tests delete bucketlist when provided valid id.
            DELETE '/bucketlists/71'
        """
        response = self.client.delete(
            reverse('api:bucketlist_detail', kwargs={'pk': 71}),
        )
        self.assertEqual(response.status_code, 204)
