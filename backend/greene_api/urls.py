from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from greene_api.views import UserCreateAPIView
from rest_framework.routers import DefaultRouter

from .views import PostViewSet


router = DefaultRouter()
router.register(r'post', PostViewSet, basename='user')

urlpatterns = [
    path('user/signup/', UserCreateAPIView.as_view()),
    path('user/token-auth/', obtain_jwt_token),
    path('user/token-refresh/', refresh_jwt_token),
    path('user/token-verify/', verify_jwt_token),
]

urlpatterns += router.urls