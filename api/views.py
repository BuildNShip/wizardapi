import json

from rest_framework.response import Response
from rest_framework.views import APIView

from .helpers import generate_unique_token
from .models import UserApis, UserApiResponses
from .serializers import UserApiValidateSerializer, UserApiListSerializer


class TokenGenerateView(APIView):

    def post(self, request):
        token = generate_unique_token()
        data = {"hasError": False, "message": "success", "token": token}
        return Response(data)


class APIRegisterView(APIView):
    """
    API for creation and updation of End points request/response
    request:{
        "token":"ZR898OBTPC",
        "api": "api/auth/login",
        "method":"POST",
        "statusCode":200,
        "params":{'username':'testuser','password':'qwerty'},
        "response":{'hasError':0,'message':'Success','auth':{'accessToken':'eubdfyndnjknim.kifdmnudinjdn.kfd'}}
        }
    """

    def post(self, request):
        request_data = request.data
        if not request_data.get('token'):
            request_data['token'] = generate_unique_token()
        if request_data.get('params'):
            params = json.dumps(request_data.get('params'))
        else:
            params = request_data.get('params')
        user_api = UserApis.objects.filter(token=request_data.get('token'), api=request_data.get('api'),
                                           method=request_data.get('method'),
                                           status_code=request_data.get('statusCode'), status=UserApis.ACTIVE,
                                           deleted_at__isnull=True)
        if user_api.exists():
            serializer = UserApiValidateSerializer(user_api.last(), data=request_data)
        else:
            serializer = UserApiValidateSerializer(data=request_data)
        if not serializer.is_valid():
            return Response({"hasError": True, "message": "Validation Error", "errors": serializer.errors})
        else:
            instance = serializer.save()
            data = UserApiListSerializer(instance, many=False).data
        data = {"hasError": False, "message": "success", "response": data}
        return Response(data)


class GetAPIResponseView(APIView):

    def post(self, request, token):
        request_data = request.data
        status_code = request.META.get('HTTP_STATUSCODE')
        method = request.method
        user_api = request.path.split('test/')[1]
        print(UserApis.objects.filter(token=token, api=user_api, method=method, status_code=status_code,
                                      deleted_at__isnull=True))
        user_api = UserApis.objects.filter(token=token, api=user_api, method=method, status_code=status_code,
                                           status=UserApis.ACTIVE, deleted_at__isnull=True)
        if user_api.exists():
            # data = UserApiListSerializer(user_api, many=True).data
            responses = []
            user_api_responses = user_api.last().responses.filter(status_code=user_api.last().status_code,
                                                                  status=UserApiResponses.ACTIVE,
                                                                  deleted_at__isnull=True)
            if user_api_responses.exists():
                for user_api_response in user_api_responses:
                    user_response = user_api_response.response.replace("\'", "\"")
                    responses.append(json.loads(user_response))
            if len(responses) == 1:
                responses = responses[0]
            return Response(responses, status=status_code)

        else:
            return Response({"hasError": False, "message": "No data found", "response": None})
        # user_response = data.get('response').replace("\'", "\"")
        # response_data = json.loads(user_response)
