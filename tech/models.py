from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    # lat = models.FloatField(gettext('Latitude'), blank=True, null=True)
    # lon = models.FloatField(gettext('Longitude'), blank=True, null=True)

def __str__(self):
    # return '%s' % self.title
    return self.title
