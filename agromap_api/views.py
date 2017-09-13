"""
Views da API rest
"""
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from agromap_api.models.user import User
from agromap_api.serializers import UserSerializer


# View para index
@csrf_exempt
def index(request):
    return JsonResponse({"Error":"Not found"}, status=404, safe=False)
