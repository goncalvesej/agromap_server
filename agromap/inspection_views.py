"""
Views de inspeções e eventos do app web (browser)
"""
from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .sessions import UserSession # Classe para manipular sessões
from .decorators import *
from agromap_api.models.inspection import Inspection
from agromap_api.models.event import Event
from agromap_api.serializers import InspectionSerializer


################################################################################
#################################INSPEÇÕES######################################
################################################################################
@csrf_exempt
@login_required
@get_request
def list_inspection(request):
    __logged_user = UserSession.GetSessionData(request)
    inspections = Inspection.get_all_obj()
    return render(request, 'inspection/list.html',
    {
        'title': 'Inspeções',
        'user':__logged_user,
        'inspections':inspections,
    })

@csrf_exempt
@login_required
@valid_request
def edit_inspection(request, id):
    __logged_user = UserSession.GetSessionData(request)
    if(request.method == 'GET'):
        __inspection = Inspection.get_by_id_obj(id)
        if(__inspection!=None):
            return render(request, 'inspection/edit.html',
            {
                'title': 'Editar inspeção',
                'user':__logged_user,
                'inspection':__inspection
            })
        inspections = Inspection.get_all_obj()
        return render(request, 'inspection/list.html',
        {
            'title': 'Inspeções',
            'msg_text':'Inspeção não encontrada!',
            'msg_type':'warning',
            'user':__logged_user,
            'inspections':inspections,
        })
    else:
        __data = request.POST
        __serializer = InspectionSerializer(data=__data)
        if(__serializer.is_valid()):
            __serializer.save()
            __msg_text = "Inspeção criada com sucesso!"
            __msg_type = "success"
        else:
            __msg_text = "Erro ao criar inspeção!"
            __msg_type = "danger"
    return render(request, 'inspection/list.html',
    {
        'title': 'Inspeções',
        'msg_text':__msg_text,
        'msg_type':__msg_type,
        'user':__logged_user,
        'inspections':inspections,
    })

# View para criar uma nova inspeção
@csrf_exempt
@login_required
@valid_request
def create_inspection(request):
    __logged_user = UserSession.GetSessionData(request)
    if(request.method == 'GET'):
        inspections = Inspection.get_all_obj()
        return render(request, 'inspection/create.html',
        {
            'title': 'Criar inspeção',
            'user':__logged_user,
        })
    else:
        __data = request.POST
        __serializer = InspectionSerializer(data=__data)
        if(__serializer.is_valid()):
            __serializer.save()
            __inspections = Inspection.get_all_obj()
            return render(request, 'inspection/list.html',
            {
                'title': 'Inspeções',
                'msg_text':'Inspeção criada com sucesso!',
                'msg_type':'success',
                'user':__logged_user,
                'inspections':__inspections
            })
        else:
            __msg = 'Erro ao criar. Atenção aos campos:<br> %s'  % __serializer.errors
            return render(request, 'inspection/create.html',
            {
                'title': 'Criar inspeção',
                'msg_text':__msg,
                'msg_type':'success',
                'user':__logged_user,
            })

# View para excluir uma inspeção
@csrf_exempt
@login_required
@get_request
def delete_inspection(request, id):
    __logged_user = UserSession.GetSessionData(request)
    __msg_text = 'Erro ao excluir!'
    __msg_type = 'danger'
    __inspection = Inspection.get_by_id_obj(id)
    if(__inspection!=None):
        if(__logged_user.id == __inspection.supervisor.id):
            try:
                if(Inspection.delete(id)):
                    __msg_text = 'Excluído com sucesso!'
                    __msg_type =  'success'
            except:
                pass
        else:
            __msg_text =  'Você precisa ser o supervisor desta inspeção para excluir!'
            __msg_type =  'warning'

    __inspections = Inspection.get_all_obj()
    return render(request, 'inspection/list.html',
    {
        'title': 'Inspeções',
        'msg_text':__msg_text,
        'msg_type':__msg_type,
        'user':__logged_user,
        'inspections':__inspections,
    })

# View para exibir mapa com os eventos
@csrf_exempt
@login_required
@get_request
def inspection_map(request, id):
    __logged_user = UserSession.GetSessionData(request)
    __inspection = Inspection.get_by_id_obj(id)
    return render(request, 'event/map.html',
    {
        'title': 'Mapa',
        'user':__logged_user,
        'inspection':__inspection,
    })

################################################################################
##################################EVENTOS#######################################
################################################################################

@csrf_exempt
@login_required
@get_request
def events_by_inspection(request, id):
    __logged_user = UserSession.GetSessionData(request)
    __events = Event.get_by_inspection_obj(id)
    __inspection = Inspection.get_by_id_obj(id)
    return render(request, 'event/events.html',
    {
        'title': 'Eventos',
        'user':__logged_user,
        'inspection':__inspection,
        'events':__events,
    })

@csrf_exempt
@login_required
@get_request
def retrieve_events(request, id):
    try:
        data = Event.get_by_inspection(id)
        if(data != None):
            return JsonResponse(data, status=200, safe=False)
        return JsonResponse(True, status=200, safe=False)
    except Exception as e:
        return JsonResponse({"Error":"Agromap: Bad request"}, status=400, safe=False)
