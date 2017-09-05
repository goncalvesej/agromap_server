from django.db import models
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from argon2 import PasswordHasher

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=20, verbose_name='Nome')
    last_name = models.CharField(max_length=60, verbose_name='Sobrenome')
    email = models.EmailField(max_length=60, unique=True, verbose_name='Email')
    password = models.CharField(max_length=255, verbose_name='Senha')
    level = models.IntegerField(default=0, verbose_name='Nível')
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
        email = user.email
        password = user['password']
        users = User.objects.filter(email=email)
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
