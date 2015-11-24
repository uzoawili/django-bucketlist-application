from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from views import UserViewSet, BucketListsView, BucketListDetailView, \
				  BucketListItemCreateView, BucketlistItemDetailView


# register the viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = router.urls

urlpatterns += [ 

	# bucket list routes:

	url(r'^bucketlists/$',	
        BucketListsView.as_view(),
        name='bucketlists'),

	url(r'^bucketlists/(?P<pk>[0-9]+)/$',
        BucketListDetailView.as_view(),
        name='bucketlist_detail'),


	# bucket list item routes:

	url(r'^bucketlists/(?P<pk>[0-9]+)/items/$',
        BucketListItemCreateView.as_view(),
        name='bucketlist_item_create'),

	url(r'^bucketlists/(?P<pk>[0-9]+)/items/(?P<item_pk>[0-9]+)/$',
        BucketlistItemDetailView.as_view(),
        name='bucketlist_item_detail'),


]