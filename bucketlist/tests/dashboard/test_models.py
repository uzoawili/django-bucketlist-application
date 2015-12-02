from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from dashboard.models import BucketList, BucketListItem


class BucketListTestCase(TestCase):
    """
    Testcase for the BucketList model.
    """
    fixtures = ['sample_data.json']

    def setUp(self):
        """
        operations to be done before every test
        """
        self.user = User.objects.get(username="uzo")
        self.bucketlist = BucketList.objects.get(pk=71)

    def test_bucket_lists_can_be_created_for_user(self):
        """
        Tests that BucketLists can be created with a name and user
        """
        bucketlist = BucketList.objects.create(
            name="Foo Foo Foo",
            created_by=self.user
        )
        self.assertEqual(type(bucketlist.id), int)

    def test_bucket_lists_cannot_be_created_without_name(self):
        """
        Tests that BucketLists cannot be created without a name
        """
        with self.assertRaises(ValidationError):
            bucketlist = BucketList.objects.create(
                created_by=self.user
            )
            bucketlist.full_clean()

    def test_bucket_lists_cannot_be_created_without_creator(self):
        """
        Tests that BucketLists cannot be created without a user
        set as the creator
        """
        with self.assertRaises(IntegrityError):
            BucketList.objects.create(
                name="Foo bucketlist"
            )

    def test_bucket_lists_items_can_be_created_for_user(self):
        """
        Tests that BucketListItem can be created with a name and bucketlist
        """
        item = BucketListItem.objects.create(
            name="Foo Item",
            bucketlist=self.bucketlist
        )
        self.assertEqual(type(item.id), int)

    def test_bucket_lists_items_cannot_be_created_without_name(self):
        """
        Tests that BucketListItem cannot be created without a name
        """
        with self.assertRaises(ValidationError):
            item = BucketListItem.objects.create(
                bucketlist=self.bucketlist
            )
            item.full_clean()

    def test_bucket_lists_items_cannot_be_created_without_creator(self):
        """
        Tests that BucketLists cannot be created without it's bucketlist set
        """
        with self.assertRaises(IntegrityError):
            BucketListItem.objects.create(
                name="Foo item"
            )
