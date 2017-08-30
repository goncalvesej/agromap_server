from rest_framework import serializers
from .models import Event

class EventSerializer(serializer.ModelSerializer):

    class Meta:
        model = Event
        # fields = '__all__'
        fields = ('id', 'title', 'description')
