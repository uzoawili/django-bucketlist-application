from django.conf.urls import url, include

from views import UserRegistrationView, BucketListsView, BucketListDetailView, \
                  BucketListItemCreateView, BucketlistItemDetailView


urlpatterns = [ 

    # user and auth routes

    url(r'^auth/register$', 
        UserRegistrationView.as_view(),
        name='auth_register'),

    url(r'^auth/login$', 
        'rest_framework_jwt.views.obtain_jwt_token', 
        name='auth_login'),

    url(r'^auth/refresh$', 
        'rest_framework_jwt.views.refresh_jwt_token', 
        name='auth_refresh'),


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


    # swagger docs:
    url(r'^docs/', include('rest_framework_swagger.urls')),


]



