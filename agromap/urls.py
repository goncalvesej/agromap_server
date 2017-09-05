from django.conf.urls import include, url
from django.contrib import admin

from agromap import views

urlpatterns = [
    url(r'^login$', views.signin, name='signin'),
    url(r'^cadastro$', views.signup, name='signup'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^cadastro$', views.signup, name='signup'),
    url(r'', views.index, name='index'),
]
