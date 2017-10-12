from django.db import models
from agromap_api.models.user import User
from agromap_api.models.inspection import Inspection

class Event(models.Model):
    uuid = models.CharField(max_length=255)
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
    description = models.CharField(max_length=255)
    kind = models.CharField(max_length=40, default='Checked')
    last_edit_at = models.DateTimeField(auto_now_add=True)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)

    def __str__(self):
        return self.uuid

    def get_by_id_json(__uuid):
        __events = Event.objects.filter(uuid=__uuid)
        if(len(__events) == 1):
            for ev in __events:
                pass
            __event = {
                'uuid':ev.uuid,
                'user':ev.user.id,
                'inspection':ev.inspection.id,
                'description':ev.description,
                'kind':ev.kind,
                'last_edit_at':str(ev.last_edit_at),
                'latitude':ev.latitude,
                'longitude':ev.longitude,
            }
            return __event
        return None

    def get_by_id_obj(__uuid):
        __events = Event.objects.filter(uuid=__uuid)
        if(len(__events) == 1):
            for ev in __events:
                return ev
        return None

    def get_by_user(__id):
        __events = Event.objects.filter(user=__id).order_by('uuid')
        if(len(__events) > 0):
            return __events
        return None

    def get_by_inspection(__id):
        __events = Event.objects.filter(inspection=__id).order_by('id')
        data = []
        if(len(__events) > 0):
            for ev in __events:
                __event = {
                    'uuid':ev.uuid,
                    'user':ev.user.id,
                    'inspection':ev.inspection.id,
                    'description':ev.description,
                    'kind':ev.kind,
                    'last_edit_at':str(ev.last_edit_at),
                    'latitude':ev.latitude,
                    'longitude':ev.longitude,
                }
                data.append(__event)
            return data
        return None
