"""
Views de usuário do app web (browser)
"""
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers

from agromap_api.models.user import User
from agromap_api.serializers import UserSerializer
from .forms import FormLogin
from .sessions import UserSession # Classe para manipular sessões
from .decorators import *
import json

@post_request
@already_logged
def signin(request):
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
                "msg_text":'Dados não conferem!',
                "msg_type":'danger',
                'form_login': form_login,
                'user':__logged_user
            })
    else: # Verificação de formulário válido
        return render(request, 'index.html', {
        "msg_text":'Atenção aos campos!',
        "msg_type":'danger',
        'form_login': form_login,
        'user':__logged_user
        })

# View para cadastro, se já logado, direciona para a Home
@already_logged
@valid_request
def signup(request):
    __logged_user = None
    form_login = FormLogin()
    if request.method == 'GET':
        return render(request,'user/signup.html',
        {
            'form_login': form_login,
            'user':__logged_user
        })
    else:
        __data = request.POST
        serializer = UserSerializer(data=__data)
        if serializer.is_valid():
            serializer.save()
            return render(request, 'index.html',
            {
                "msg_text":'Criado com sucesso!',
                "msg_type":'primary',
                'form_login': form_login,
                'user':__logged_user
            })
        __msg ='Atenção aos campos: %s' % serializer.errors
        return render(request, 'index.html',
        {
        "msg_text":__msg,
        "msg_type":'danger',
        'form_login':form_login,
        'user':__logged_user
        })

# View para logout
@get_request
def logout(request):
    form_login = FormLogin()
    __logged_user = None
    UserSession.KillSession(request)
    return render(request, 'index.html',
    {
        'form_login': form_login,
        'user':__logged_user
    })

# View para alterar senha
@login_required
@post_request
def change_password(request):
    __data = request.POST
    __logged_user = UserSession.GetSessionData(request)
    __logged_user_data = User.get_by_id(__logged_user.id)
    __new_password = __data['new_password']
    __old_password = __data['old_password']
    user = {
        'email': __logged_user_data.email,
        'password': __old_password,
        'new_password': __new_password
    }
    if User.signin(user):
        if User.update_password(user):
            return render(request, 'user/my-data.html',
            {
                "title":"Meus dados",
                "msg_text":'Senha atualizada com sucesso!',
                "msg_type":'primary',
                'user':__logged_user_data
            })
        return render(request, 'user/my-data.html',
        {
        "title":"Meus dados",
        "msg_text":"Houve um erro interno!",
        "msg_type":'danger',
        'user':__logged_user_data
        })
    return render(request, 'my-data.html',
    {
    "title":"Meus dados",
    "msg_text":"Senha atual não confere!",
    "msg_type":'warning',
    'user':__logged_user_data
    })

# View para meus dados
@login_required
@get_request
def my_data(request):
    __logged_user = UserSession.GetSessionData(request)
    __logged_user_data = User.get_by_id(__logged_user.id)
    return render(request, 'user/my-data.html',
    {
        'title': 'Meus dados',
        'user':__logged_user_data
    })

@login_required
@admin_required
def list_users(request):
    __logged_user = UserSession.GetSessionData(request)
    users = User.get_all()
    return render(request, 'user/list-users.html',
    {
        'title': 'Gerenciar usuários',
        'user':__logged_user,
        'users': users
    })

@login_required
@admin_required
def delete_user(request, id):
    __logged_user = UserSession.GetSessionData(request)
    __text = ""
    __type = ""
    if(User.delete(id)):
        __text = "Usuário excluído com sucesso!"
        __type = "success"
    else:
        __text = "Erro ao excluir!"
        __type = "danger"
    users = User.get_all()
    return render(request, 'user/list-users.html',
    {
        'title': 'Gerenciar usuários',
        'msg_type': __type,
        'msg_text': __text,
        'user':__logged_user,
        'users': users
    })
