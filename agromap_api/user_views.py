"""
Views da API rest (app mobile)
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

# View para logar usuário, retorna objeto user com id, nome, nivel e  email ou False
# Espera-se um JSON com um objeto user com dois valores:
# email e password
@csrf_exempt
def signin(request):
    if request.method == 'POST':
        __data = json.loads(request.POST['user'])
        __logged_user = User.signin(__data)
        if __logged_user != None:
            jsonObj = {
                'id':__logged_user['id'],
                'name':__logged_user['name'],
                'email':__logged_user['email'],
                'level':__logged_user['level']
            }
            return JsonResponse(jsonObj, status=200, safe=False)
        return JsonResponse(False, status=401, safe=False)
    else:
        return JsonResponse({"Error":"HTTP method not allowed"}, status=405, safe=False)



# View para cadastrar usuário, retorna True/False ou a lista dos erros
# Espera-se um JSON com um objeto user com todos valores da classe User
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        __data = json.loads(request.POST['user'])
        serializer = UserSerializer(data=__data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(True, status=201, safe=False)
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=400, safe=False)
    else:
        return JsonResponse({"Error":"HTTP method not allowed"}, status=405, safe=False)

# View para atualizar usuário (nome e sobrenome), retorna True ou a lista dos erros
# Espera-se um JSON com um objeto user com todos valores da classe User
# Não altera o email e senha, estes possuem suas prórprias views
@csrf_exempt
def update(request):
    if request.method == 'POST':
        __data = json.loads(request.POST['user'])
        if User.signin(__data):
            if User.update(__data):
                return JsonResponse(True, status=200, safe=False)
            else:
                return JsonResponse({"Error":"Email not found"}, status=400, safe=False)
        return JsonResponse({"Error":"Incorrect password"}, status=400)
    else:
        return JsonResponse({"Error":"HTTP method not allowed"}, status=405, safe=False)

# View para alterar o email do usuário e retorna True ou a lista dos erros
# Espera-se um JSON com um objeto user com todos os valores
# id e novo email. Irá localizar o usuário pelo ID e substituir o email
@csrf_exempt
def update_email(request):
    if request.method == 'POST':
        data = json.loads(request.POST['user'])
        if User.signin(data):
            if User.update_email(data):
                return JsonResponse(True, status=200, safe=False)
            else:
                return JsonResponse({"Error":"Email not found"}, status=400)
        return JsonResponse({"Error":"Incorrect password"}, status=400)
    else:
        return JsonResponse({"Error":"HTTP method not allowed"}, status=405, safe=False)

# View para alterar a senha do usuário e retorna True ou a lista dos erros
# Espera-se um JSON com um objeto user com todos os valores:
# email, senha e nova senha. Irá localizar o usuário pelo email e substituir a senha
@csrf_exempt
def update_password(request):
    if request.method == 'POST':
        data = json.loads(request.POST['user'])
        if User.signin(data):
            if User.update_password(data):
                return JsonResponse(True, status=200, safe=False)
            else:
                return JsonResponse({"Error":"Email not found"}, status=400)
        return JsonResponse({"Error":"Incorrect password"}, status=400)
    else:
        return JsonResponse({"Error":"HTTP method not allowed"}, status=405, safe=False)

# View para retornar o ID do usuário
# Espera-se um JSON com um objeto user com todos os valores:
# email
@csrf_exempt
def get_ID(request):
    if request.method == 'POST':
        data = json.loads(request.POST['user'])
        if User.signin(data):
            __id = User.get_ID(data)
            if __id:
                return JsonResponse({"id":__id}, status=200, safe=False)
            else:
                return JsonResponse({"Error":"Email not found"}, status=400)
    else:
        return JsonResponse({"Error":"HTTP method not allowed"}, status=405, safe=False)
