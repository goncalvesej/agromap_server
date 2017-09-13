from django.conf.urls import include, url
from django.contrib import admin

from agromap_api import inspection_views

urlpatterns = [

    url(r'^create$', inspection_views.create, name='create-inspection'),
    url(r'^update$', inspection_views.update, name='update-inspection'),
    url(r'^delete$', inspection_views.delete, name='delete-inspection'),
    url(r'^get$', inspection_views.get, name='get-inspection'),
    url(r'', inspection_views.index, name='index'),
]
