from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from dashboard.views import IndexView


urlpatterns = [

	# admin
	url(r'^admin/', include(admin.site.urls)),

	# bucketlist web dashboard:
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^signout/$', auth_views.logout_then_login, name='signout'),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),

    # bucketlist api:
    url(r'^api/', include('api.urls', namespace='api')),

]


    