from django.conf.urls import include, url
from django.contrib import admin

from agromap_api import views

urlpatterns = [

    url(r'^user/', include('agromap_api.user_urls')),
    url(r'^inspection/', include('agromap_api.inspection_urls')),
    url(r'', views.index, name='index'),
]
