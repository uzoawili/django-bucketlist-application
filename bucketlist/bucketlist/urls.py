from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from dashboard.views import IndexView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^signout/$', auth_views.logout_then_login, name='signout')
]
