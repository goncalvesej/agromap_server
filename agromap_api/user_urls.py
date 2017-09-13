from django.conf.urls import include, url
from django.contrib import admin

from agromap_api import views, user_views

urlpatterns = [

    url(r'^signup$', user_views.signup, name='signup'),
    url(r'^signin$', user_views.signin, name='signin'),
    url(r'^update$', user_views.update, name='update'),
    url(r'^update-email$', user_views.update_email, name='update_email'),
    url(r'^update-password$', user_views.update_password, name='update_password'),
    url(r'', views.index, name='index'),
]
