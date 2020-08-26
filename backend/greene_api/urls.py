from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

# from greene_api.views import UserCreateAPIView
from rest_framework.routers import DefaultRouter

from .views import UserViewSet ,PostViewSet

urlpatterns = []

user_router = DefaultRouter()
post_router = DefaultRouter()
user_router.register(r'user', UserViewSet, basename='user')
post_router.register(r'post', PostViewSet, basename='post')


urlpatterns += user_router.urls
urlpatterns += post_router.urls
urlpatterns += [
    path('token/', obtain_jwt_token),
    path('token/refresh/', refresh_jwt_token),
    path('token/verify/', verify_jwt_token),
]
