from django.db import models
from agromap_api.models.user import User
from agromap_api.models.inspection import Inspection

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        Inspection,
        on_delete = models.SET_DEFAULT,
        blank=False,
        null=False,
        default = 0
    )
    inspection_id = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        blank=False,
        null=False,
    )
    typeof = models.IntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edit_at = models.DateTimeField(auto_now_add=True)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)

    def __str__(self):
        # return '%s' % self.title
        return self.id
