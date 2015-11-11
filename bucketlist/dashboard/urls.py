from django.conf.urls import url
from views import IndexView, BucketListsView

urlpatterns = [
    url(r'^bucketlists/$', BucketListsView.as_view(), name='bucketlists'),
]
