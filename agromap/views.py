"""
Views do app web (browser)
"""
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_http_methods

from agromap_api.models.user import User
from agromap_api.serializers import UserSerializer
from .forms import FormLogin
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


def about(request):
    form_login = FormLogin()
    __logged_user = None
    if UserSession.IsActive(request):
        __logged_user = UserSession.GetSessionData(request)
    return render(request, 'about.html',
    {
        'form_login': form_login,
        'user':__logged_user
    })
