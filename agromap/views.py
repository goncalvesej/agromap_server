"""
Views do app web (browser)
"""

from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers

from agromap_api.models.user import User
from agromap_api.serializers import UserSerializer
from .forms import FormLogin, FormUser
from .sessions import UserSession # Classe para manipular sessões

# View da página index
def index(request):
    form_login = FormLogin()
    __logged_user = None
    if UserSession.IsActive(request):
        __logged_user = UserSession.GetSessionData(request)
    return render(request, 'index.html',
    {
        'form_login': form_login,
        'user':__logged_user
    })

# View para login, se já logado, direciona para Home
def signin(request):
    __logged_user = None
    form_login = FormLogin()
    if request.method == 'POST':
        if UserSession.IsActive(request):
            __logged_user = UserSession.GetSessionData(request)
            return render(request, 'home.html', {
                'user':__logged_user
            })
        form_login = FormLogin(request.POST)
        if form_login.is_valid():
            user = {
                'email': request.POST['email'],
                'password':request.POST['password']
            }
            __logged_user = User.signin(user)
            if(__logged_user != None):
                UserSession.SaveSession(request, __logged_user)
                return render(request, 'home.html', {
                    'user':__logged_user
                })
            else: # Se método de login do model retornar None o login é inválido
                return render(request, 'index.html', {
                    "text":'Dados não conferem!',
                    "msg_type":'danger',
                    'form_login': form_login,
                    'user':__logged_user
                })
        else: # Verificação de formulário válido
            return render(request, 'index.html', {
            "text":'Atenção aos campos!',
            "msg_type":'danger',
            'form_login': form_login,
            'user':__logged_user
            })

    else: # Se método HTTP não for post, direciona para Index
        return render(request, 'index.html', {
        'form_login': form_login,
        'user':__logged_user
        })


# View para cadastro, se já logado, direciona para a Home
def signup(request):
    __logged_user = None
    if UserSession.IsActive(request): # Já logado
        __logged_user = UserSession.GetSessionData(request)
        return render(request, 'home.html', {
            'user':__logged_user,
        })

    form_login = FormLogin()
    form_user = FormUser()
    if request.method == 'GET':
        return render(request,'signup.html',
        {
            'form_user': form_user,
            'form_login': form_login,
            'user':__logged_user
        })
    elif request.method == 'POST':
        __data = request.POST
        serializer = UserSerializer(data=__data)
        if serializer.is_valid():
            serializer.save()
            return render(request, 'index.html',
            {
                "text":'Criado com sucesso!',
                "msg_type":'primary',
                'form_login': form_login,
                'user':__logged_user
            })
        __msg ='Atenção aos campos: %s' % serializer.errors
        return render(request, 'index.html',
        {
        "text":__msg,
        "msg_type":'danger',
        'form_login':form_login,
        'user':__logged_user
        })
    else: # Se método HTTP não for post ou get, direciona para Index
        return render(request, 'index.html', {
        'form_login': form_login,
        'user':__logged_user
        })

# View para logout
def logout(request):
    if request.method == 'GET':
        form_login = FormLogin()
        __logged_user = None
        UserSession.KillSession(request)
        return render(request, 'index.html',
        {
            'form_login': form_login,
            'user':__logged_user

        })
    else: # Se método HTTP não for get, direciona para Index
        return render(request, 'index.html', {
        'form_login': form_login,
        'user':__logged_user
        })
