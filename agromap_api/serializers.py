from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from argon2 import PasswordHasher
from agromap_api.models.user import User
from agromap_api.models.inspection import Inspection
from agromap_api.models.event import Event


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'last_name', 'email', 'level','password','created_at')

    def create(self, validated_data):
        hash = self.hashpass(validated_data['password'])
        validated_data['password'] = hash
        return User.objects.create(**validated_data)

    def update(self, validated_data):
        hash = self.hashpass(validated_data['password'])
        validated_data['password'] = hash
        return User.objects.update(**validated_data)

    def hashpass(self, pwd):
        ph = PasswordHasher()
        return ph.hash(pwd)

class InspectionSerializer(ModelSerializer):
    class Meta:
        model = Inspection
        fields = ('id', 'name', 'created_at', 'start_at', 'end_at','supervisor')

class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ('uuid', 'user', 'last_edit_at', 'inspection', 'description', 'kind', 'latitude', 'longitude')
