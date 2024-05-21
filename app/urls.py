"""Contains all of the urls used in the app."""

#url pattern
from django.urls import re_path
from django.views.static import serve
from django.conf import settings

from app.transducer import views
from app.transducer import views_others


# pylint:disable=C0103
app_name = 'app'
urlpatterns = [
    # Example:
    re_path(r'^$', views.index, name='index'),
    re_path(r'^$', views_others.index, name='index'),
    re_path(r'^independence/?$', views.upload_file, name='independence'),
    re_path(r'^others/?$', views_others.upload_file, name='others'),
    re_path(r'^transducer/?$', views.upload_file, name='transducer'),
    re_path(r'^media/([0-9]+.zip)$', \
        serve, \
        {'document_root': settings.MEDIA_ROOT})

]
