from __future__ import absolute_import

from django.contrib.auth import update_session_auth_hash
from rest_framework.serializers import ModelSerializer, CharField

from app.models.user import User, Company

class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class UserSerializer(ModelSerializer):
    password = CharField(write_only = True, required = False)
    confirm_password = CharField(required = False)
    company = CompanySerializer(many = False, read_only = True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'confirm_password', 'company', 'token')
        read_only_fields = ('confirm_password', 'company')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


