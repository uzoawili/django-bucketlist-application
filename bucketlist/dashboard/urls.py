from django.conf.urls import url
from views import IndexView, BucketListsView, \
	 BucketListCreateView, BucketListUpdateView, \
	 BucketListDeleteView, BucketListDetailView, \
	 BucketListItemCreateView, BucketListItemUpdateView, \
	 BucketListItemDoneView, BucketListItemDeleteView

urlpatterns = [
	
	# bucket list routes:

    url(r'^bucketlists/$', \
    	BucketListsView.as_view(), \
    	name='bucketlists'),

    url(r'^bucketlists/create/$', \
    	BucketListCreateView.as_view(), \
    	name='bucketlist_create'),

    url(r'^bucketlists/(?P<pk>[0-9]+)/update/$', \
    	BucketListUpdateView.as_view(), \
    	name='bucketlist_update'),

    url(r'^bucketlists/(?P<pk>[0-9]+)/delete/$', \
    	BucketListDeleteView.as_view(), \
    	name='bucketlist_delete'),

    url(r'^bucketlists/(?P<pk>[0-9]+)/$', 
    	BucketListDetailView.as_view(), \
    	name='bucketlist_details'),
    

    # bucket list item routes:
    
    url(r'^bucketlists/(?P<pk>[0-9]+)/items/create$', \
    	BucketListItemCreateView.as_view(), \
    	name='bucketlist_item_create'),

    url(r'^bucketlists/(?P<pk>[0-9]+)/items/(?P<item_pk>[0-9]+)/update/$', \
    	BucketListItemUpdateView.as_view(), \
    	name='bucketlist_item_update'),

    url(r'^bucketlists/(?P<pk>[0-9]+)/items/(?P<item_pk>[0-9]+)/done/$', \
        BucketListItemDoneView.as_view(), \
        name='bucketlist_item_done'),

    url(r'^bucketlists/(?P<pk>[0-9]+)/items/(?P<item_pk>[0-9]+)/delete/$', \
    	BucketListItemDeleteView.as_view(), \
    	name='bucketlist_item_delete'),

    
]
