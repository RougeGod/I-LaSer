#url pattern
from django.conf.urls import url
from django.views.static import serve
from transducer import views
from transducer import viewsOthers
from django.conf import settings


app_name = 'app'

urlpatterns = [
    # Example:
    url(r'^$', views.index, name='index'),
    url(r'^$', viewsOthers.index, name='index'),
    url(r'^independence/$', views.upload_file, name='independence'),
    url(r'^others/$', viewsOthers.upload_file, name='others'),
    url(r'^transducer/$', views.upload_file, name='transducer'),
    url(r'^media/([0-9]+.zip)$', \
        serve, \
        {'document_root': settings.MEDIA_ROOT})

]
