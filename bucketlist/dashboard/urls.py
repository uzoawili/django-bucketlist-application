from django.conf.urls import url
from views import IndexView, BucketListsView, \
	 BucketListCreateView, BucketListUpdateView, \
	 BucketListDeleteView

urlpatterns = [
    url(r'^bucketlists/$', BucketListsView.as_view(), name='bucketlists'),
    url(r'^bucketlists/create/$', BucketListCreateView.as_view(), name='bucketlist_create'),
    url(r'^bucketlists/(?P<pk>[0-9]+)/update/$', BucketListUpdateView.as_view(), name='bucketlist_update'),
    url(r'^bucketlists/(?P<pk>[0-9]+)/delete/$', BucketListDeleteView.as_view(), name='bucketlist_delete'),
]
