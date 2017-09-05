from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from argon2 import PasswordHasher
from agromap_api.models.user import User


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

    # def signin(self, validated_data):
    #     users = User.objects.filter(email=validated_data.email)
    #     ph = PasswordHasher()
    #     for u in users:
    #         if ph.verify(user.password, password):
    #             return True
    #     return False
