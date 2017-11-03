"""
Views da API rest (app mobile)
"""
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.utils.six import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
import numpy
import datetime

from agromap_api.models.inspection import Inspection
from agromap_api.models.event import Event
from agromap_api.models.device import Device
from agromap_api.serializers import InspectionSerializer
from agromap_api.serializers import EventSerializer

# View para index
@csrf_exempt
def index(request):
    return JsonResponse({"Error":"Agromap: Not found"}, status=404, safe=False)

# TODO
# Header Authorization
@csrf_exempt
def create(request):
    if request.method == 'POST':
        __data = json.loads(request.POST['inspection'])
        serializer = InspectionSerializer(data=__data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(True, status=201, safe=False)
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=400, safe=False)
    else:
        return JsonResponse({"Error":"Agromap: HTTP method not allowed"}, status=405, safe=False)

# TODO
# Header Authorization
@csrf_exempt
def update(request):
    if request.method == 'POST':
        try:
            __data = json.loads(request.POST['inspection'])
            __inspection = Inspection.get_by_id_obj(__data['id'])
            serializer = InspectionSerializer(__inspection, data=__data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(True, status=201, safe=False)
            print(serializer.errors)
            return JsonResponse(serializer.errors, status=400, safe=False)
        except Exception as e:
            return JsonResponse({"Error":"Agromap: Bad request"}, status=400, safe=False)
    else:
        return JsonResponse({"Error":"Agromap: HTTP method not allowed"}, status=405, safe=False)


# TODO
# Header Authorization e delete via GET
#
@csrf_exempt
def delete(request):
    if request.method == 'POST':
        __data = json.loads(request.POST['inspection'])
        __id = __data['id']
        delete_inspection_folder(__id)
        if(Inspection.delete(__id)):
            delete_inspection_folder(id)
            return JsonResponse(True, status=200, safe=False)
        return JsonResponse({"Error":"Inspection not found"}, status=405, safe=False)
    else:
        return JsonResponse({"Error":"Agromap: HTTP method not allowed"}, status=405, safe=False)

# TODO
# Header Authorization
@csrf_exempt
def get_by_id(request, id=None):
    if request.method == 'GET':
        try:
            __inspection = Inspection.get_by_id_json(id)
            if(__inspection != None):
                return JsonResponse(json.dumps(__inspection), status=200, safe=False)
            return JsonResponse({"Error":"Inspection not found"}, status=400, safe=False)
        except Exception as e:
            return JsonResponse({"Error":"Agromap: Bad request"}, status=400, safe=False)
    return JsonResponse({"Error":"Agromap: HTTP method not allowed"}, status=405, safe=False)

# TODO
# Header Authorization
@csrf_exempt
def get_all(request, id=None):
    if request.method == 'GET':
        try:
            data = Inspection.get_all()
            if(data != None):
                return JsonResponse(data, status=200, safe=False)
            return JsonResponse(True, status=200, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"Error":"Agromap: Bad request"}, status=400, safe=False)
    return JsonResponse({"Error":"Agromap: HTTP method not allow    ed"}, status=405, safe=False)

# TODO
# Header Authorization
@csrf_exempt
def get_by_supervisor(request, id=None):
    if request.method == 'GET':
        try:
            data = Inspection.get_by_supervisor(id)
            if(data != None):
                return JsonResponse(data, status=200, safe=False)
            return JsonResponse({"Error":"None inspection from supervisor"}, status=400, safe=False)
        except Exception as e:
            return JsonResponse({"Error":"Agromap: Bad request"}, status=400, safe=False)
    return JsonResponse({"Error":"Agromap: HTTP method not allowed"}, status=405, safe=False)

@csrf_exempt
def create_events(request):
    if request.method == 'POST':
        __data = json.loads(request.POST['event'])
        for __event in __data:
            if( __event['latitude'] == 'delete'):
                try:
                    event_to_delete = Event.get_by_id_obj(__event['uuid'])
                    event_to_delete.delete()
                except:
                    pass
            else:
                __event_obj = Event.get_by_id_obj(__event['uuid'])
                if(__event_obj != None):
                    serializer = EventSerializer(__event_obj, data=__event)
                else:
                    serializer = EventSerializer(data=__event)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
                    return JsonResponse("False", status=400, safe=False)
        return JsonResponse("True", status=201, safe=False)
    else:
        return JsonResponse({"Error":"Agromap: HTTP method not allowed"}, status=405, safe=False)


@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        __data = json.loads(request.POST['event'])
        serializer = EventSerializer(data=__data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(True, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400, safe=False)
    else:
        return JsonResponse({"Error":"Agromap: HTTP method not allowed"}, status=405, safe=False)


@csrf_exempt
def update_event(request):
    if request.method == 'POST':
        __data = json.loads(request.POST['event'])
        __event = Event.get_by_id_obj(__data['uuid'])
        serializer = EventSerializer(__event, data=__data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(True, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400, safe=False)
    else:
        return JsonResponse({"Error":"Agromap: HTTP method not allowed"}, status=405, safe=False)

# TODO
# Header Authorization e delete via GET
#
@csrf_exempt
def delete_event(request):
    if request.method == 'POST':
        __data = json.loads(request.POST['event'])
        __event = Event.get_by_id_obj(__data['uuid'])
        if(__event != None):
            __event.delete()
            return JsonResponse(True, status=200, safe=False)
        return JsonResponse({"Error":"Inspection not found"}, status=405, safe=False)
    else:
        return JsonResponse({"Error":"Agromap: HTTP method not allowed"}, status=405, safe=False)

# TODO
# Header Authorization
#
@csrf_exempt
def get_event_by_id(request, uuid=None):
    if request.method == 'GET':
        try:
            __event = Event.get_by_id_json(uuid)
            if(__event != None):
                return JsonResponse(json.dumps(__event), status=200, safe=False)
            return JsonResponse({"Error":"Event not found"}, status=400, safe=False)
        except Exception as e:
            return JsonResponse({"Error":"Agromap: Bad request"}, status=400, safe=False)
    return JsonResponse({"Error":"Agromap: HTTP method not allowed"}, status=405, safe=False)

# TODO
# Header Authorization
#
@csrf_exempt
def get_event_by_inspection(request, id=None):
    if request.method == 'GET':
        try:
            data = Event.get_by_inspection(id)
            if(data != None):
                return JsonResponse(data, status=200, safe=False)
            return JsonResponse(True, status=200, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"Error":"Agromap: Bad request"}, status=400, safe=False)
    return JsonResponse({"Error":"Agromap: HTTP method not allowed"}, status=405, safe=False)

# TODO
# Header Authorization
#
@csrf_exempt
def get_event_by_user(request, id=None):
        if request.method == 'GET':
            try:
                __events = Event.get_by_user(id)
                if(__events != None):
                    data = serializers.serialize('json', __events)
                    return JsonResponse(data, status=200, safe=False)
                return JsonResponse({"Error":"None event from user"}, status=400, safe=False)
            except Exception as e:
                return JsonResponse({"Error":"Agromap: Bad request"}, status=400, safe=False)
        return JsonResponse({"Error":"Agromap: HTTP method not allowed"}, status=405, safe=False)

@csrf_exempt
def get_uuid(request):
    try:
        exit = False
        new_uuid = ''
        while exit != True:
            new_uuid = Device.get_new_uuid()
            if(Device.check(new_uuid)):
                exit = True
        device = Device()
        device.uuid = new_uuid
        device.save()
        return JsonResponse({"UUID":new_uuid}, status=201, safe=False)
    except:
        pass



##
##
##


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
        print(e)
    return False

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
        print(e)
    return False
