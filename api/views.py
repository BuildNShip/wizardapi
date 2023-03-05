import json

from rest_framework.response import Response
from rest_framework.views import APIView

from .helpers import generate_unique_token
from .models import UserApis
from .serializers import UserApiValidateSerializer


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
	"params":"{'username':'testuser','password':'qwerty'}",
	"response":"{'hasError':0,'message':'Success','auth':{'accessToken':'eubdfyndnjknim.kifdmnudinjdn.kfd'}}"
}
    """

    def post(self, request):
        request_data = request.data
        if not request_data.get('token'):
            request_data['token'] = generate_unique_token()
        user_api = UserApis.objects.filter(token=request_data.get('token'), api=request_data.get('api'),
                                           method=request_data.get('method'))
        if user_api.exists():
            serializer = UserApiValidateSerializer(user_api.last(), data=request_data)
        else:
            serializer = UserApiValidateSerializer(data=request_data)
        if not serializer.is_valid():
            return Response({"hasError": True, "message": "Validation Error", "errors": serializer.errors})
        else:
            instance = serializer.save()
            data = UserApiValidateSerializer(instance, many=False).data
        data = {"hasError": False, "message": "success", "response": data}
        return Response(data)


class GetAPIResponseView(APIView):

    def post(self, request, token):
        request_data = request.data
        method = request.method
        user_api = request.path.split('test/')[1]
        user_api = UserApis.objects.filter(token=token, api=user_api, method=method)
        if user_api.exists():
            data = UserApiValidateSerializer(user_api.last(), many=False).data
        else:
            return Response({"hasError": False, "message": "No data found", "response": None})
        user_response = data.get('response').replace("\'", "\"")
        response_data = json.loads(user_response)
        return Response(response_data)
