from django.urls import path,  re_path
from .views import TokenGenerateView, APIRegisterView, GetAPIResponseView

urlpatterns = [
    path('generate-token', TokenGenerateView.as_view(), name="generate_token"),
    path('end-point/register', APIRegisterView.as_view(), name="api_register"),
    re_path('test/.*', GetAPIResponseView.as_view(), name="get_api_response"),
]