from django.conf.urls import include, url
from django.contrib import admin

from agromap import views, user_views, inspection_views

urlpatterns = [
    # Usuario
    url(r'^login$', user_views.signin, name='signin'),
    url(r'^cadastro$', user_views.signup, name='signup'),
    url(r'^logout$', user_views.logout, name='logout'),
    url(r'^cadastro$', user_views.signup, name='signup'),
    url(r'^meus-dados$', user_views.my_data, name='my_data'),
    url(r'^alterar-senha$', user_views.change_password, name='change-password'),
    url(r'^gerenciar-usuarios$', user_views.list_users, name='list-users'),
    url(r'^usuario/excluir/(\d+)$', user_views.delete_user, name='delete-user'),

    # Inspeções e eventos
    url(r'^inspecao$', inspection_views.list_inspection, name='list-inspection'),
    url(r'^inspecao/lista$', inspection_views.list_inspection, name='list-inspection2'),
    url(r'^inspecao/criar$', inspection_views.create_inspection, name='create-inspection'),
    url(r'^inspecao/(\d+)/excluir$', inspection_views.delete_inspection, name='delete-inspection'),
    url(r'^inspecao/(\d+)/editar$', inspection_views.edit_inspection, name='edit-inspection'),
    url(r'^inspecao/(\d+)/eventos$', inspection_views.events_by_inspection, name='events-by-inspection'),
    url(r'^inspecao/(\d+)/mapa$', inspection_views.inspection_map, name='inspection-map'),
    url(r'^retrieve-events/(\d+)', inspection_views.retrieve_events, name='retrieve_events'),
    url(r'^evento/(?P<uuid>[\w-]+)/excluir', inspection_views.delete_event, name='delete_event'),

    url(r'', views.index, name='index'),
]
