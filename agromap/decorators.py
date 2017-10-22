from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from .sessions import UserSession
from .forms import FormLogin

def login_required(function):
    def wrap(request, *args, **kwargs):
        if UserSession.IsActive(request):
            return function(request, *args, **kwargs)
        else:
            __logged_user = None
            form_login = FormLogin()
            return render(request, 'index.html', {
                "msg_text":'Necessário estar logado!',
                "msg_type":'warning',
                'form_login': form_login,
                'user':__logged_user
            })
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def post_request(function):
    def wrap(request, *args, **kwargs):
        if request.method == 'POST':
            return function(request, *args, **kwargs)
        else:
            return redirect('/')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def get_request(function):
    def wrap(request, *args, **kwargs):
        if request.method == 'GET':
            return function(request, *args, **kwargs)
        else:
            return redirect('/')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def valid_request(function):
    def wrap(request, *args, **kwargs):
        if request.method == 'GET' or request.method == 'POST':
            return function(request, *args, **kwargs)
        else:
            return redirect('/')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def already_logged(function):
    def wrap(request, *args, **kwargs):
        if UserSession.IsActive(request):
            return redirect('/home')
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


# Decorator para verificar se usuário logado é admin
def admin_required(function):
    def wrap(request, *args, **kwargs):
        form_login = FormLogin()
        __logged_user = UserSession.GetSessionData(request)
        if(__logged_user.level == 0):
            return function(request, *args, **kwargs)
        else:
            return render(request, 'index.html', {
                "msg_text":'Você não tem permissão para acessar esta página!',
                "msg_type":'danger',
                'form_login': form_login,
                'user':__logged_user
            })
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
