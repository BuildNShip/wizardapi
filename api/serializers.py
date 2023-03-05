from django.core.validators import EmailValidator
from rest_framework import serializers

from api.models import UserApis


class UserApiValidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserApis
        fields = ['api', 'method', 'params', 'response', 'token']
