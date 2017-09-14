from django.db import models
from agromap_api.models.user import User
import numpy

class Inspection(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20,null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    start_at = models.DateTimeField(null=False)
    end_at = models.DateTimeField(null=False)
    supervisor = models.ForeignKey(
        User,
        on_delete = models.SET_DEFAULT,
        blank=False,
        null=False,
        default = 0
    )
    members = models.ManyToManyField(User)

    def __str__(self):
        # return '%s' % self.title
        return self.name

    def get_by_id_json(__id):
        __inspections = Inspection.objects.filter(id=__id)
        if(len(__inspections) == 1):
            for i in __inspections:
                pass
            __inspection = {
                'id':i.id,
                'name':i.name,
                'created_at':str(i.created_at),
                'start_at':str(i.start_at),
                'end_at':str(i.end_at),
                'supervisor':i.supervisor.id,
            }
            return __inspection
        return None

    def get_by_id_obj(__id):
        __inspections = Inspection.objects.filter(id=__id)
        if(len(__inspections) == 1):
            for i in __inspections:
                return i
        return None


    def get_by_supervisor(supervisor_id):
        __inspections = Inspection.objects.filter(supervisor=supervisor_id)
        if(len(__inspections) > 0):
            return __inspections
        return False
