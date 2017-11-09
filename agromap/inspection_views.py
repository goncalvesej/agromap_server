"""
Views de inspeções e eventos do app web (browser)
"""
from django.shortcuts import render
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .sessions import UserSession # Classe para manipular sessões
from .decorators import *
from agromap_api.models.inspection import Inspection
from agromap_api.models.event import Event
from agromap_api.serializers import InspectionSerializer
import boto3
import datetime


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

def teste(request):
    return render(request, 'home.html',
    {
        'title': 'Inspeções',

    })


# View para criar uma nova inspeção
@csrf_exempt
@login_required
@admin_required
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
        if(__data['start_at'] > __data['end_at']):
            return render(request, 'inspection/create.html',
            {
                'title': 'Inspeções',
                'msg_text':'Data de início deve ser anterior a data de término!',
                'msg_type':'warning',
                'user':__logged_user,
            })
        __serializer = InspectionSerializer(data=__data)
        if(__serializer.is_valid()):
            print(__data)
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
                    delete_inspection_folder(id)
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

@csrf_exempt
@login_required
@valid_request
def edit_inspection(request, id):
    __logged_user = UserSession.GetSessionData(request)
    if(request.method == 'GET'):
        __inspection = Inspection.get_by_id_obj(id)
        if(__inspection!=None):
            # Start date
            day = '%02d' % (__inspection.start_at.day)
            month = '%02d' % (__inspection.start_at.month)
            year = str(__inspection.start_at.year)

            dateStart = day + '/' + month + '/' + year
            dateStart_formated = year + '-' + month + '-' + day + 'T00:00:00-00'

            # End date
            day = '%02d' % (__inspection.end_at.day)
            month = '%02d' % (__inspection.end_at.month)
            year = str(__inspection.end_at.year)

            dateEnd = day + '/' + month + '/' + year
            dateEnd_formated = year + '-' + month + '-' + day + 'T23:59:59-00'

            return render(request, 'inspection/edit.html',
            {
                'title': 'Editar inspeção',
                'user':__logged_user,
                'inspection':__inspection,
                'dateStart':dateStart,
                'dateStart_formated':dateStart_formated,
                'dateEnd':dateEnd,
                'dateEnd_formated':dateEnd_formated
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
        __inspection = Inspection.get_by_id_obj(__data['id'])
        if(__inspection == None):
            __msg_text = 'Inspeção não encontrada!'
            __msg_type = 'warning'
        else:
            print(__data['start_at'])
            print(__data['end_at'])
            __inspection.name = __data['name']
            __inspection.start_at = __data['start_at']
            __inspection.end_at = __data['end_at']
            __serializer = InspectionSerializer(__inspection, data=__data)
            if(__serializer.is_valid()):
                __serializer.save()
                __msg_text = "Inspeção alterada com sucesso!"
                __msg_type = "success"
            else:
                __msg_text = "Erro ao criar inspeção. Verifique os campos!"
                __msg_type = "danger"
                print(__serializer.errors)

        inspections = Inspection.get_all_obj()
        return render(request, 'inspection/list.html',
        {
            'title': 'Inspeções',
            'msg_text':__msg_text,
            'msg_type':__msg_type,
            'user':__logged_user,
            'inspections':inspections,
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
def delete_event(request, uuid):
    __logged_user = UserSession.GetSessionData(request)
    __event = Event.get_by_id_obj(uuid)
    __msg_text = "Evento não encontrado!"
    __msg_type = "warning"
    if(__event == None):
        __inspections = Inspection.get_all_obj()
        return render(request, 'inspection/list.html',
        {
            'title': 'Lista de Inspeções',
            'user':__logged_user,
            'inspections':__inspections,
            'msg_text':__msg_text,
            'msg_type':__msg_type
        })
    __inspection = __event.inspection
    __msg_text = "Você precisa ser o administrador da inspeção para excluir"
    __msg_type = "warning"
    if(__logged_user.id == __event.inspection.supervisor.id):
        try:
            delete_photo(str(__event.inspection.id) + '/' + __event.uuid + '.png')
            __event.delete()
            __msg_text = "Excluído com sucesso!"
            __msg_type = "success"
        except Exception as e:
            print(e)
            __msg_text = "Erro ao excluir!"
            __msg_type = "danger"

    __events = Event.get_by_inspection_obj(__inspection.id)
    return render(request, 'event/events.html',
    {
        'title': 'Eventos',
        'user':__logged_user,
        'inspection':__inspection,
        'events':__events,
        'msg_text':__msg_text,
        'msg_type':__msg_type
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

# Exclui foto do S3 de um determinado evento
def delete_photo(__key):
    try:
        __s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        response = __s3_client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key= __key
        )
        return True
    except Exception as e:
        pass
    return False

# Exclui o diretório de fotos de uma inspeção
def delete_inspection_folder(__id):
    try:
        __s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        __objects = __s3_client.list_objects(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Prefix=__id + '/'
        )
        for obj in __objects['Contents']:
            delete_photo(obj['Key'])
        return True
    except Exception as e:
        pass
    return False
