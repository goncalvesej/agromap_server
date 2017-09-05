from django.conf.urls import include, url
from django.contrib import admin

from agromap_api import views

urlpatterns = [

    url(r'^signup$', views.signup, name='signup'),
    url(r'^signin$', views.signin, name='signin'),
    url(r'^update$', views.update, name='update'),
    url(r'^update-email$', views.update_email, name='update_email'),
    url(r'^update-password$', views.update_password, name='update_password'),
    url(r'', views.index, name='index'),
]
