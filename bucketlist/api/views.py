from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from dashboard.models import BucketList, BucketListItem
from serializers import BucketListSerializer, BucketListDetailSerializer, \
                        BucketListItemSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset for User model.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()



class BucketListsView(generics.ListCreateAPIView):
    """
    Returns a list of bucketlists created by the authenticated in user
    or creates a new bucklist.
    """
    serializer_class = BucketListSerializer

    def get_queryset(self):
        """ 
        Returns the queryset of bucketlists created by the current user. 
        """
        # get any search param from the request:
        query_params = self.request.query_params
        # get user's bucketlists:
        results = BucketList.objects.filter(created_by=self.request.user)
        # search if param is specified:
        search_query = query_params.get('q')
        if search_query:
            results = results.filter(name__icontains=search_query)

        return results



class BucketListDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates or deletes a bucketlist.
    """
    serializer_class = BucketListDetailSerializer

    def get_queryset(self):
        # get user's bucketlists:
        return BucketList.objects.filter(created_by=self.request.user)



class BucketListItemEditMixin(object):
    """
    Mixin defining common methods and vars needed for
    creating, updating and deleting BucketListItems.
    """
    serializer_class = BucketListItemSerializer

    def get_current_bucketlist(self):
        """ Returns the bucketlist refrenced in the url """
        return get_object_or_404(
            BucketList,
            created_by=self.request.user, 
            pk=self.kwargs.get('pk')
        )

    def get_queryset(self):
        bucketlist = get_current_bucketlist()
        return BucketListItem.objects.filter(bucketlist=bucketlist)



class BucketListItemCreateView(generics.CreateAPIView, BucketListItemEditMixin):
    """
    Creates a BucketList item.
    """
    def perform_create(self, serializer):
        serializer.save(bucketlist=get_current_bucketlist())

    

class BucketlistItemDetailView(mixins.UpdateModelMixin, 
    mixins.DestroyModelMixin, generics.GenericAPIView,
    BucketListItemEditMixin):
    """
    Reads, Updates, or Deletes a BucketList item.
    """
    def get_object(self):
        bucketlist = get_current_bucketlist()
        return get_object_or_404(
            BucketlistItem,
            bucketlist=bucketlist,
            pk=self.kwargs.get('pk_item')
        )



















