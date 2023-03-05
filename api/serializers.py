import json

from rest_framework import serializers

from api.models import UserApis, UserApiResponses
from django.core.exceptions import MultipleObjectsReturned


class UserApiValidateSerializer(serializers.ModelSerializer):
    response = serializers.JSONField(required=True)
    params = serializers.JSONField(required=True)
    statusCode = serializers.IntegerField(source='status_code')

    class Meta:
        model = UserApis
        fields = ['api', 'method', 'params', 'response', 'token', 'statusCode']

    def create(self, validated_data):
        responses = validated_data.pop('response')
        status_code = validated_data.get('status_code')
        params = validated_data.pop('params')
        validated_data['params'] = json.dumps(params)
        user_api_obj = UserApis.objects.create(**validated_data)
        if type(responses) is list:
            for response in validated_data.get('response'):
                response = json.dumps(response)
                UserApiResponses.objects.create(user_api=user_api_obj,
                                                status_code=status_code, response=response)
        else:
            response = json.dumps(responses)
            UserApiResponses.objects.create(user_api=user_api_obj,
                                            status_code=status_code, response=response)
        return user_api_obj

    def update(self, instance, validated_data):
        responses = validated_data.pop('response')
        status_code = validated_data.get('status_code')
        params = validated_data.pop('params')
        validated_data['params'] = json.dumps(params)
        super(UserApiValidateSerializer, self).update(instance, validated_data)
        instance.responses.filter(status=UserApiResponses.ACTIVE, deleted_at__isnull=True).update(
            status=UserApiResponses.INACTIVE)
        if type(responses) is list:
            for response in responses:
                response = json.dumps(response)
                try:
                    user_api_response, created = UserApiResponses.objects.get_or_create(user_api=instance,
                                                                                        status_code=status_code,
                                                                                        response=response,
                                                                                        deleted_at__isnull=True)
                except MultipleObjectsReturned:
                    UserApiResponses.objects.filter(user_api=instance, status_code=status_code, response=response,
                                                    deleted_at__isnull=True).delete()
                    UserApiResponses.objects.create(user_api=instance, status_code=status_code, response=response,
                                                    deleted_at__isnull=True)
                if not created:
                    # user_api_response.response = response
                    user_api_response.status = UserApiResponses.ACTIVE
                    user_api_response.save()
        else:
            response = json.dumps(responses)
            try:
                user_api_response, created = UserApiResponses.objects.get_or_create(user_api=instance,
                                                                                    status_code=status_code,
                                                                                    response=response,
                                                                                    deleted_at__isnull=True)
            except MultipleObjectsReturned:
                UserApiResponses.objects.filter(user_api=instance, status_code=status_code, response=response,
                                                deleted_at__isnull=True).delete()
                UserApiResponses.objects.create(user_api=instance, status_code=status_code, response=response,
                                                deleted_at__isnull=True)
            if not created:
                # user_api_response.response = response
                user_api_response.status = UserApiResponses.ACTIVE
                user_api_response.save()
        return instance


class UserApiListSerializer(serializers.ModelSerializer):
    response = serializers.SerializerMethodField()
    params = serializers.SerializerMethodField()
    statusCode = serializers.IntegerField(source='status_code')

    class Meta:
        model = UserApis
        fields = ['api', 'method', 'params', 'response', 'token', 'statusCode']

    def get_response(self, obj):
        responses = []
        user_api_responses = obj.responses.filter(status_code=obj.status_code, status=UserApiResponses.ACTIVE,
                                                  deleted_at__isnull=True)
        if user_api_responses.exists():
            for user_api_response in user_api_responses:
                user_response = user_api_response.response.replace("\'", "\"")
                responses.append(json.loads(user_response))
        if len(responses) == 1:
            responses = responses[0]
            # user_response = user_response.replace("\'", "\"")
            # responses.append(user_response)
        return responses

    def get_params(self, obj):
        params = obj.params.replace("\'", "\"")
        params = json.loads(params)
        return params


class GetUserApiDataSerializer(serializers.ModelSerializer):
    response = serializers.SerializerMethodField()
    # params = serializers.SerializerMethodField()
    # statusCode = serializers.IntegerField(source='status_code')

    class Meta:
        model = UserApis
        fields = ['response']

    def get_response(self, obj):
        responses = []
        user_api_responses = obj.responses.filter(status_code=obj.status_code, status=UserApiResponses.ACTIVE,
                                                  deleted_at__isnull=True)
        if user_api_responses.exists():
            for user_api_response in user_api_responses:
                user_response = user_api_response.response.replace("\'", "\"")
                responses.append(json.loads(user_response))
        if len(responses) == 1:
            responses = responses[0]
        return responses

    def get_params(self, obj):
        params = obj.params.replace("\'", "\"")
        params = json.loads(params)
        return params

