from django.db import models
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from argon2 import PasswordHasher

class User(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=20, verbose_name='Nome')
    last_name = models.CharField(max_length=60, verbose_name='Sobrenome')
    email = models.EmailField(max_length=60, unique=True, verbose_name='Email')
    password = models.CharField(max_length=255, verbose_name='Senha')
    level = models.IntegerField(default=2, max_length=20, verbose_name='Nível')
    active = models.CharField(max_length=10, verbose_name='Ativo', default='false')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    def __str__(self):
        # return '%s' % self.title
        return self.name

    # Login
    # Tenta efetuar pelo id (esta forma é utilizada para alterar o email)
    # Se falhar, tenta pelo email (dessa forma é feito o login normal)
    def signin(user):
        __password = user['password']
        try:
            __id = user['id']
            users = User.objects.filter(id=__id)
        except:
            try:
                __email = user['email']
                users = User.objects.filter(email=__email)
            except:
                pass
        ph = PasswordHasher()
        for u in users:
            if(u.active == 'false'):
                return None
            try:
                ph.verify(u.password, __password)
                __logged_user = {
                     'id':u.id,
                     'name':u.name,
                     'email':u.email,
                     'level':u.level
                }
                return __logged_user
            except:
                return None

    # Atualiza nome e sobrenome
    def update(user):
        __email = user['email']
        password = user['password']
        users = User.objects.filter(email=__email)
        ph = PasswordHasher()
        for u in users:
            u.name = user['name']
            u.last_name = user['last_name']
            u.save()
            return True
        False

    # Altera email, busca do registro é feita pelo ID
    def update_email(user):
        __id = user['id']
        users = User.objects.filter(id=__id)
        for u in users:
            u.email = user['email']
            u.save()
            return True
        False

    # Atualiza senha. Este método é chamado após verificar o login mediante a senha antiga
    def update_password(user):
        email = user['email']
        new_password = user['new_password']
        users = User.objects.filter(email=email)
        ph = PasswordHasher()
        new_password =  ph.hash(new_password)
        for u in users:
            u.password = new_password
            u.save()
            return True
        return False

    # Devolve ID do usuário, busca feita por email. Necessário o ID para atualizar o email
    def get_ID(user):
        email = user['email']
        users = User.objects.filter(email=email)
        for u in users:
            return u.id
        return False

    def get_by_id(__id):
        users = User.objects.filter(id=__id)
        if (len(users) < 1):
            return None
        for user in users:
            user.password = "************"
            return user

    def get_all():
        return User.objects.all().order_by('id')

    def delete(__id):
        try:
            User.objects.filter(id=__id).delete()
            return True
        except:
            pass
        return False

    def changeActive(__id):
        try:
            users = User.objects.filter(id=__id)
            for u in users:
                if(u.active =='true'):
                    u.active = 'false'
                else:
                    u.active = 'true'
                u.save()
                return True
            return False
        except Exception as e:
            print(e)
            pass
        return False

    def changeLevel(__id):
        try:
            __user = User.objects.filter(id=__id)
            __user = __user[0]
            if(__user.level == 0):
                users = User.objects.all()
                nAdmin = 0
                for u in users:
                    if(u.level == 0):
                        nAdmin = nAdmin + 1
                if(nAdmin > 1):
                    __user.level = 2
                    __user.save()
                    return True
                return False
            else:
                __user.level = 0
                __user.save()
                return True
        except Exception as e:
            print(e)
            return False

    def updateData(__data, __id):
        try:
            __user = User.objects.filter(id=__id)
            __user = __user[0]
            __user.name = __data['name']
            __user.last_name = __data['last_name']
            __user.email = __data['email']
            __user.save()
            return True
        except Exception as e:
            print(e)
            return False
