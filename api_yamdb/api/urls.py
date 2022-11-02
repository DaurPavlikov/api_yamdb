from django.urls import path
from .views import SignupViewSet, TokenViewSet


urlpatterns = [
    path('v1/auth/signup/', SignupViewSet.as_view(
        {'post': 'create'}
    ), name='signup'),
    path('v1/auth/token/', TokenViewSet.as_view(
        {'post': 'gettoken'}
    ), name='token'),
]
