from django.db import models
from agromap_api.models.user import User
from agromap_api.models.inspection import Inspection

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete = models.SET_DEFAULT,
        blank=False,
        null=False,
        default = 0
    )
    inspection = models.ForeignKey(
        Inspection,
        on_delete = models.CASCADE,
        blank=False,
        null=False,
    )
    types = models.IntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edit_at = models.DateTimeField(auto_now_add=True)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)

    def __str__(self):
        # return '%s' % self.title
        return self.id

    def get_by_id_json(__id):
        __events = Event.objects.filter(id=__id)
        if(len(__events) == 1):
            for ev in __events:
                pass
            __event = {
                'id':ev.id,
                'user':ev.user.id,
                'inspection':ev.inspection.id,
                'types':ev.types,
                'description':ev.description,
                'created_at':str(ev.created_at),
                'last_edit_at':str(ev.last_edit_at),
                'latitude':ev.latitude,
                'longitude':ev.longitude,
            }
            return __event
        return None

    def get_by_id_obj(__id):
        __events = Event.objects.filter(id=__id)
        if(len(__events) == 1):
            for ev in __events:
                return ev
        return None

    def get_by_user(__id):
        __events = Event.objects.filter(user=__id).order_by('id')
        if(len(__events) > 0):
            return __events
        return None

    def get_by_inspection(__id):
        __events = Event.objects.filter(inspection=__id).order_by('id')
        data = []
        if(len(__events) > 0):
            for ev in __events:
                __event = {
                    'id':ev.id,
                    'user':ev.user.id,
                    'inspection':ev.inspection.id,
                    'types':ev.types,
                    'description':ev.description,
                    'created_at':str(ev.created_at),
                    'last_edit_at':str(ev.last_edit_at),
                    'latitude':ev.latitude,
                    'longitude':ev.longitude,
                }
                data.append(__event)
            return data
        return None
