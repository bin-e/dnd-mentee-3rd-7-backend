from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserViewSet ,PostViewSet

urlpatterns = []

user_router = DefaultRouter()
post_router = DefaultRouter()
user_router.register(r'user', UserViewSet, basename='user')
post_router.register(r'post', PostViewSet, basename='post')


urlpatterns += user_router.urls
urlpatterns += post_router.urls
urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
