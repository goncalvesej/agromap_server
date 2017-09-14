from django.conf.urls import include, url
from django.contrib import admin

from agromap_api import inspection_views

urlpatterns = [
    url(r'^create$', inspection_views.create, name='create-inspection'),
    url(r'^update$', inspection_views.update, name='update-inspection'),
    url(r'^delete$', inspection_views.delete, name='delete-inspection'),
    url(r'^get-all$', inspection_views.get_all, name='get-all'),
    url(r'^get-by-id/(\d+)$', inspection_views.get_by_id, name='get-inspection-by-id'),
    url(r'^get-by-supervisor/(\d+)$', inspection_views.get_by_supervisor, name='get-inspection-by-sup'),
    url(r'^create-event$', inspection_views.create_event, name='create-event'),
    url(r'^update-event$', inspection_views.update_event, name='update-event'),
    url(r'^delete-event$', inspection_views.delete_event, name='delete-event'),
    url(r'^get-event-by-id/(\d+)$', inspection_views.get_event_by_id, name='get-event-by-id'),
    url(r'^get-event-by-user/(\d+)$', inspection_views.get_event_by_user, name='get-event-by-user'),
    url(r'^get-event-by-inspection/(\d+)$', inspection_views.get_event_by_inspection, name='get-event-by-inspection'),
    url(r'', inspection_views.index, name='index'),
]
