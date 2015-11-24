from django.contrib.auth.models import User
from rest_framework import serializers

from dashboard.models import BucketList, BucketListItem
from serializer_utils import ParameterisedHyperlinkedIdentityField



class UserSerializer(serializers.ModelSerializer):
    """
    API serializer for the User model.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'bucketlists_url')

    bucketlists_url = ParameterisedHyperlinkedIdentityField(
      view_name='api:bucketlists',
      lookup_fields=()
    )
    


class BucketListItemSerializer(serializers.ModelSerializer):
    """
    API serializer for the BucketListItem model.
    """
    class Meta:
        model = BucketListItem
        fields = ('id', 'name', 'description', 'date_created', 
                  'date_modified','done', 'url')

    url = ParameterisedHyperlinkedIdentityField(
      view_name='api:bucketlist_item_detail',
      lookup_fields=(('bucketlist.pk', 'pk'), ('pk', 'item_pk'))
    )



class BucketListSerializer(serializers.ModelSerializer):
    """
    API serializer for the BucketList model without its items.
    """
    class Meta:
        model = BucketList
        fields = ('id', 'name', 'description', 'date_created', 
                  'date_modified', 'created_by', 'num_items',
                  'num_done_items', 'url')

    created_by = UserSerializer()
    url = serializers.HyperlinkedIdentityField(view_name='api:bucketlist_detail')



class BucketListDetailSerializer(BucketListSerializer):
    """
    API serializer for the BucketList model along with its items.
    """
    class Meta:
        model = BucketList
        fields = ('id', 'name', 'description', 'date_created', 
                  'date_modified', 'created_by', 'items', 'url', 
                  'create_item_url')

    items = BucketListItemSerializer(many=True, read_only=True)
    create_item_url = serializers.HyperlinkedIdentityField(view_name='api:bucketlist_item_create')

