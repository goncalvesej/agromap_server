
"""
Classe para manipular sessões
"""

from agromap_api.models.user import User

class UserSession():

    #Recebe objeto User que será salvo na sessão
    def SaveSession(request, user):
        request.session['user'] ={
            'id':user['id'],
            'name':user['name'],
            'email':user['email'],
            'level':user['level']
        }

    #Verifica se sessão está ativa
    def IsActive(request):
        try:
            id = request.session['user']['id']
            return True
        except:
            return False

    #Retorna objeto User que está salvo na sessão
    def GetSessionData(request):
        return User(
            id=request.session['user']['id'],
            name=request.session['user']['name'],
            email=request.session['user']['email'],
            )

    #Destrói a sessão
    def KillSession(request):
        try:
            del request.session['user']
        except Exception as ex:
            print(ex)
            pass
