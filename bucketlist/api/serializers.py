from django.contrib.auth.models import User
from rest_framework import serializers
from dashboard.models import BucketList, BucketListItem


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    API serializer for the User model.
    """
    class Meta:
        model = User
        fields = ('id', 'username',)

    bucketlists = serializers.HyperlinkedIdentityField(view_name='bucketlists')
    


class BucketListSerializer(serializers.HyperlinkedModelSerializer):
    """
    API serializer for the BucketList model without its items.
    """
    class Meta:
        model = Bucketlist
        fields = ('id', 'name', 'description', \
                  'date_created', 'date_modified', \
                  'created_by', 'num_items',
                  'num_done_items', 'url')

    created_by = UserSerializer()



class BucketListDetailSerializer(BucketListSerializer):
    """
    API serializer for the BucketList model.
    """
    class Meta:
        model = Bucketlist
        fields = ('id', 'name', 'description', \
                  'date_created', 'date_modified', \
                  'created_by', 'items', 'url')

    items = BucketListItemSerializer(many=True, read_only=True)
 


class BucketListItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    API serializer for the BucketListItem model.
    """
    class Meta:
        model = BucketListItem
        fields = ('id', 'name', 'description', \
                  'date_created', 'date_modified', \
                  'created_by', 'done', 'url')




