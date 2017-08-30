from django.conf.urls import include, url

from django.contrib import admin

import tech.views

urlpatterns = [
    url(r'^', tech.views.index, name='index'),
]
