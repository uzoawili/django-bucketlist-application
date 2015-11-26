from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings

from dashboard.models import BucketList, BucketListItem
from serializers import BucketListSerializer, BucketListDetailSerializer, \
    BucketListItemSerializer, UserSerializer


class UserRegistrationView(generics.CreateAPIView):

    """
    View for registering users.
    Registration params: 'username' and 'password'
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Creates a new user and generates an authentication token
        to automatically log them in.
        """
        # process the registration params:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # automatically get token for the created user/log them in:
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)
        # get the response headers:
        headers = self.get_success_headers(serializer.data)
        # prepare the response body:
        body = {
            'token': token,
            'user': serializer.data,
        }
        return Response(body, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        self.user = serializer.save()


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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


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
        bucketlist = self.get_current_bucketlist()
        return BucketListItem.objects.filter(bucketlist=bucketlist)


class BucketListItemCreateView(
    BucketListItemEditMixin,
    generics.CreateAPIView
):
    """
    Creates a BucketList item.
    """

    def perform_create(self, serializer):
        serializer.save(bucketlist=self.get_current_bucketlist())


class BucketlistItemDetailView(
    BucketListItemEditMixin,
    generics.RetrieveUpdateDestroyAPIView
):

    """
    Updates, or Deletes a BucketList item.
    """

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['item_pk'])
        return obj
