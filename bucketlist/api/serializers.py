from django.contrib.auth.models import User
from rest_framework import serializers
from dashboard.models import BucketList, BucketListItem


class UserSerializer(serializers.ModelSerializer):
    """
    API serializer for the User model.
    """
    class Meta:
        model = User
        fields = ('id', 'username',)

    # bucketlists = serializers.HyperlinkedIdentityField(view_name='api:bucketlists')
 


class BucketListItemSerializer(serializers.ModelSerializer):
    """
    API serializer for the BucketListItem model.
    """
    class Meta:
        model = BucketListItem
        fields = ('id', 'name', 'description', 'date_created', 
                  'date_modified','done')



class BucketListSerializer(serializers.ModelSerializer):
    """
    API serializer for the BucketList model without its items.
    """
    class Meta:
        model = BucketList
        fields = ('id', 'name', 'description', 'date_created', 
                  'date_modified', 'created_by', 'num_items',
                  'num_done_items',)

    created_by = UserSerializer()



class BucketListDetailSerializer(BucketListSerializer):
    """
    API serializer for the BucketList model along with its items.
    """
    class Meta:
        model = BucketList
        fields = ('id', 'name', 'description', 'date_created', 
                  'date_modified', 'created_by', 'items',)

    items = BucketListItemSerializer(many=True, read_only=True)


