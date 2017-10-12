from django.db import models
import random
import string

class Device(models.Model):
    uuid = models.CharField(max_length=20, verbose_name='UUID')

    def __str__(self):
        return self.uuid


    # Verifica se já exite uuid
    def check(__uuid):
        try:
            __devices = Device.objects.filter(uuid=__uuid)
            if(__devices.count() > 0):
                return False
            return True
        except Exception as e:
            print(e)
            return True

    def get_new_uuid():
        chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        __new_uuid = ''
        i = 0
        while i < 4:
            __new_uuid = __new_uuid + random.choice(chars)
            i = i + 1
        return __new_uuid
