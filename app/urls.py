"""Contains all of the urls used in the app."""

#url pattern
from django.conf.urls import url
from django.views.static import serve
from django.conf import settings

from app.transducer import views
from app.transducer import views_others


# pylint:disable=C0103
app_name = 'app'
urlpatterns = [
    # Example:
    url(r'^$', views.index, name='index'),
    url(r'^$', views_others.index, name='index'),
    url(r'^independence/$', views.upload_file, name='independence'),
    url(r'^others/$', views_others.upload_file, name='others'),
    url(r'^transducer/$', views.upload_file, name='transducer'),
    url(r'^media/([0-9]+.zip)$', \
        serve, \
        {'document_root': settings.MEDIA_ROOT})

]
